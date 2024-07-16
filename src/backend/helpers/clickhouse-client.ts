// @ts-nocheck
import axios, { AxiosRequestConfig } from 'axios';
import * as https from 'https';
import { URL } from 'url';
import {logger} from '@grafana/ts-backend';

export interface Settings {
    Instance: {
        URL: string;
        BasicAuthEnabled: boolean;
        DecryptedSecureJSONData: { [key: string]: string };
        BasicAuthUser: string;
    };
    UsePost: boolean;
    UseCompression: boolean;
    CompressionType: string;
    UseYandexCloudAuthorization: boolean;
    XHeaderUser: string;
    XHeaderKey: string;
    TLSSkipVerify: boolean;
}

interface Response {
    ctx: any;
    body: any;
    // other properties
}

export class ClickhouseClient {
    settings: Settings;

    constructor(settings: Settings) {
        this.settings = settings;
    }

    async query(ctx: any, query: string): Promise<Response> {
        const onErr = (err: Error): never => {
            console.error(`clickhouse client query error: ${err}`);
            throw err;
        };

        let datasourceUrl: URL;
        try {
            datasourceUrl = new URL(this.settings.Instance.URL);
        } catch (err) {
            return onErr(new Error(`unable to parse clickhouse datasource url: ${err}`));
        }

        const httpsAgentOptions: https.AgentOptions = {};
        let reqConfig: AxiosRequestConfig = {
            url: datasourceUrl.toString(),
            method: this.settings.UsePost ? 'POST' : 'GET',
            data: this.settings.UsePost ? query : undefined,
            params: !this.settings.UsePost ? { query } : undefined,
            headers: {},
            httpsAgent: new https.Agent(httpsAgentOptions)
        };

        if (this.settings.UseCompression && ['gzip', 'br', 'deflate', 'zstd'].includes(this.settings.CompressionType)) {
            reqConfig.headers['Accept-Encoding'] = this.settings.CompressionType;
            reqConfig.params = { ...reqConfig.params, enable_http_compression: '1' };
        }

        if (this.settings.Instance.BasicAuthEnabled) {
            const password = this.settings.Instance.DecryptedSecureJSONData['basicAuthPassword'];
            reqConfig.auth = {
                username: this.settings.Instance.BasicAuthUser,
                password
            };
        } else if (this.settings.UseYandexCloudAuthorization) {
            reqConfig.headers['X-ClickHouse-User'] = this.settings.XHeaderUser;
            if (this.settings.XHeaderKey) {
                reqConfig.headers['X-ClickHouse-Key'] = this.settings.XHeaderKey;
            }
            const password = this.settings.Instance.DecryptedSecureJSONData['xHeaderKey'];
            if (password) {
                reqConfig.headers['X-ClickHouse-Key'] = password;
            }
        }

        logger.info('Work with settings', this.settings)
        const tlsCACert = this.settings.Instance?.DecryptedSecureJSONData?.tlsCACert
        const tlsClientCert = this.settings.Instance?.DecryptedSecureJSONData?.tlsClientCert
        const tlsClientKey = this.settings.Instance?.DecryptedSecureJSONData?.tlsClientKey

        if (tlsCACert) {
            httpsAgentOptions.ca = tlsCACert;
        }

        if (tlsClientCert && tlsClientKey) {
            httpsAgentOptions.cert = tlsClientCert;
            httpsAgentOptions.key = tlsClientKey;
        } else if (tlsClientCert || tlsClientKey) {
            return onErr(new Error('please setup both tlsClientCert and tlsClientKey'));
        }

        if (this.settings.TLSSkipVerify) {
            httpsAgentOptions.rejectUnauthorized = false;
        }

        let resp;
        try {
            logger.info('Clickhouse request', reqConfig)
            resp = await axios.request(reqConfig);
            let body: string;

            if (['gzip', 'deflate', 'br', 'zstd'].includes(resp.headers['content-encoding'])) {
                body = await new Promise((resolve, reject) => {
                    let buffer: Buffer[] = [];
                    resp.data.on('data', (chunk: Buffer) => buffer.push(chunk));
                    resp.data.on('end', () => resolve(Buffer.concat(buffer).toString()));
                    resp.data.on('error', (err: Error) => reject(err));
                });
            } else {
                logger.info('no encoding')
                body = resp.data;
            }

            logger.info('Clickhouse response', resp.status, body)
            if (resp.status !== 200) {
                return onErr(new Error(body));
            }

            const jsonResp: { ctx: any; body: any } = { ctx, body: body};
            return jsonResp;
        } catch (err) {
            return onErr(err as Error);
        }
    }
}