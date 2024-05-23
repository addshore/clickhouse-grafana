import React, { useEffect, useState } from 'react';
import { QueryEditorProps } from '@grafana/data';
import { CHDataSource } from '../../datasource/datasource';
import { CHDataSourceOptions, CHQuery, EditorMode } from '../../types/types';
import { QueryHeader } from './components/QueryHeader/QueryHeader';
import { QueryTextEditor } from './components/QueryTextEditor/QueryTextEditor';
import { QueryBuilder } from './components/QueryBuilder/QueryBuilder';
import SqlQuery from '../../datasource/sql-query/sql_query';
import { Alert } from "@grafana/ui";
import {useSystemDatabases} from "../hooks/useSystemDatabases";
import {useAutocompleteData} from "../hooks/useAutocompletionData";

const defaultQuery = 'SELECT $timeSeries as t, count() FROM $table WHERE $timeFilter GROUP BY t ORDER BY t';
const DEFAULT_FORMAT = 'time_series';
const DEFAULT_DATE_TIME_TYPE = 'DATETIME';
const DEFAULT_ROUND = '0s';
const DEFAULT_INTERVAL_FACTOR = 1;

function useFormattedData(query: CHQuery, datasource: CHDataSource): [string, string | null] {
  useSystemDatabases(datasource)
  useAutocompleteData(datasource)
  const [formattedData, setFormattedData] = useState(query.query);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    try {
      if (datasource.options && datasource.templateSrv) {
        const queryModel = new SqlQuery(query, datasource.templateSrv, datasource.options);
        // @ts-ignore
        const adhocFilters = datasource.templateSrv.getAdhocFilters(datasource.name);
        const replaced = queryModel.replace(datasource.options, adhocFilters);
        setFormattedData(replaced);
        setError(null);
      }
    } catch (e: any) {
      setError(e?.message);
    }
  }, [query, datasource.name, datasource.options, datasource.templateSrv]);

  return [formattedData, error];
}

export function QueryEditor(props: QueryEditorProps<CHDataSource, CHQuery, CHDataSourceOptions>) {
  const { datasource, query, onChange, onRunQuery } = props;
  const isAnnotationView = !props.app;
  const [editorMode, setEditorMode] = useState(EditorMode.Builder);
  const initializedQuery = initializeQueryDefaults(query, isAnnotationView, datasource);
  const [formattedData, error] = useFormattedData(initializedQuery, datasource);
  const [datasourceName] = useState(datasource.name);

  useEffect(() => {
    // On component mount
    const storedData = localStorage.getItem('datasourceInfo');
    if (storedData) {
      const { name, timestamp } = JSON.parse(storedData);
      const currentTime = new Date().getTime();
      const timeDifference = (currentTime - timestamp) / 1000; // Convert milliseconds to seconds

      if (timeDifference < 5) {
        if (name !== datasourceName) {

          const initialQuery = {
            ...query,
            format: DEFAULT_FORMAT,
            extrapolate: true,
            skip_comments: true,
            add_metadata: true,
            dateTimeType: DEFAULT_DATE_TIME_TYPE,
            round: DEFAULT_ROUND,
            intervalFactor: DEFAULT_INTERVAL_FACTOR,
            interval: '',
            query: defaultQuery,
            formattedQuery: query.query,
            editorMode: EditorMode.Builder,
            database: undefined,
            table: undefined,
            dateColDataType: undefined,
            dateTimeColDataType: undefined,
          };

          onChange(initialQuery);
        }
      }
    }

    // On component unmount
    return () => {
      const dataToStore = {
        name: datasourceName,
        timestamp: new Date().getTime()
      };
      localStorage.setItem('datasourceInfo', JSON.stringify(dataToStore));
    };
    // eslint-disable-next-line
  }, []);

  const onSqlChange = (sql: string) => onChange({ ...initializedQuery, query: sql });

  const onFieldChange = (value: any) => onChange({ ...query, ...value });

  const onTriggerQuery = () => onRunQuery()

  return (
    <>
      <QueryHeader query={initializedQuery} editorMode={editorMode} setEditorMode={setEditorMode} isAnnotationView={isAnnotationView} onTriggerQuery={onTriggerQuery} />
      {error ? <Alert title={error} elevated style={{marginTop: "5px", marginBottom: "5px"}}/> : null}
      {editorMode === EditorMode.Builder && (
        <QueryBuilder query={initializedQuery} datasource={datasource} onChange={(items: CHQuery) => onChange({...items})} onRunQuery={onTriggerQuery} />
      )}
      {editorMode === EditorMode.SQL && (
        <>
          <QueryTextEditor
            query={initializedQuery}
            height={200}
            onSqlChange={onSqlChange}
            onRunQuery={onTriggerQuery}
            onFieldChange={onFieldChange}
            formattedData={formattedData}
            datasource={datasource}
            isAnnotationView={isAnnotationView}
          />
        </>
      )}
    </>
  );
}

function initializeQueryDefaults(query: CHQuery, isAnnotationView: boolean, datasource: any): CHQuery {
  console.log(datasource.defaultValues, '-----------')
  const initializedQuery = {
    ...query,
    format: query.format || DEFAULT_FORMAT,
    extrapolate: query.extrapolate ?? true,
    skip_comments: query.skip_comments ?? true,
    add_metadata: query.add_metadata ?? true,
    dateTimeType: query.dateTimeType || DEFAULT_DATE_TIME_TYPE,
    round: query.round || DEFAULT_ROUND,
    intervalFactor: query.intervalFactor || DEFAULT_INTERVAL_FACTOR,
    interval: query.interval || '',
    query: query.query || defaultQuery,
    formattedQuery: query.formattedQuery || query.query,
    editorMode: EditorMode.Builder
  };

  enum DateTimeType {
    DateTime = 'DATETIME',
    DateTime64 = 'DATETIME64',
    TimeStamp = 'TIMESTAMP'
  }

  if (datasource.defaultValues) {
    console.log(datasource.defaultValues)
    console.log(datasource.defaultValues.dateTime.defaultDateTime, initializedQuery.dateTimeType === DateTimeType.DateTime, !initializedQuery.dateTimeColDataType)
    if (datasource.defaultValues.dateTime.defaultDateTime && initializedQuery.dateTimeType === DateTimeType.DateTime && !initializedQuery.dateTimeColDataType) {
      initializedQuery.dateTimeColDataType = datasource.defaultValues.dateTime.defaultDateTime;
    }

    if (datasource.defaultValues.dateTime.defaultDateTime64 && initializedQuery.dateTimeType === DateTimeType.DateTime64 && !initializedQuery.dateTimeColDataType) {
      initializedQuery.dateTimeColDataType = datasource.defaultValues.dateTime.defaultDateTime64;
    }

    if (datasource.defaultValues.dateTime.defaultDateDate32 && !initializedQuery.dateColDataType) {
      initializedQuery.dateColDataType = datasource.defaultValues.dateTime.defaultDateDate32;
    }

    if (datasource.defaultValues.dateTime.defaultUint32 && initializedQuery.dateTimeType === DateTimeType.TimeStamp  && !initializedQuery.dateTimeColDataType) {
      initializedQuery.dateTimeColDataType = datasource.defaultValues.dateTime.defaultUint32;
    }
  }

  if (isAnnotationView) {
    initializedQuery.format = 'ANNOTATION'
  }

  return initializedQuery
}
