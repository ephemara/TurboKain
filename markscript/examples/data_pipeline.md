# DataPipeline

A streaming data pipeline: ingest, transform, validate, write.

## ingest_stream

> open kafka consumer
> poll batch records
> deserialize protobuf

| Topic        | Partition | Offset  | Lag   |
|-------------|-----------|---------|-------|
| events.raw  | 0         | 1500000 | 1200  |
| events.raw  | 1         | 1498000 | 3400  |
| events.raw  | 2         | 1501200 | 800   |
| events.dlq  | 0         | 45000   | 0     |

## transform_batch

> apply schema mapping
> enrich with lookup
> filter invalid records

| Transform         | Records_In | Records_Out | Latency_ms |
|-------------------|------------|-------------|------------|
| SchemaMapping     | 50000      | 49800       | 12         |
| GeoEnrichment     | 49800      | 49800       | 45         |
| Deduplication     | 49800      | 47200       | 28         |
| NullFilter        | 47200      | 46800       | 3          |

## validate_output

> check schema constraints
> verify referential integrity
> sign batch checksum

| Constraint       | Passed  | Failed | Skipped |
|------------------|---------|--------|---------|
| NotNull          | 46800   | 0      | 0       |
| UniqueKey        | 46750   | 50     | 0       |
| ForeignKey       | 46750   | 0      | 0       |
| RangeCheck       | 46700   | 50     | 0       |
| ChecksumVerify   | 46800   | 0      | 0       |

## write_sink

> flush to parquet
> update catalog
> emit metrics

| Sink          | Rows    | Size_MB | Time_ms |
|---------------|---------|---------|---------|
| ParquetMain   | 46700   | 234     | 890     |
| ParquetArchive| 46700   | 234     | 1200    |
| IcebergCatalog| 1       | 0.05    | 45      |
| Prometheus    | 12      | 0.01    | 2       |
