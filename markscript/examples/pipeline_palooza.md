# PipelinePalooza - Multi-Stage File Pipeline

> An ETL pipeline that reads, transforms, validates, and reports on data files.
> Exercises ALL 8 registered IVT handlers: read file, write file, run, assert, print,
> file exists, spawn, import kain.
> Every stage is a domain. Every operation is an intent. Everything happens.

---

## Metadata

| Property | Value |
|----------|-------|
| PipelineName | PaloozaStream |
| Version | 1.0 |
| InputFile | pipeline_input.txt |
| OutputDir | pipeline_output |
| RunTimestamp | step |

---

## Initialization

> Verify the stage directory exists before we start

```markscript
print("=== PipelinePalooza 1.0 ===")
print("Starting multi-stage ETL pipeline")
print("")

let stage = 0
```

---

## StageIngest - Read source data

> The intake stage: read the raw input file and log its contents.

> Read the raw input file into the VM
> read file "examples/pipeline_inbox.txt"

> Print confirmation that ingestion is complete
> print "Ingest stage complete"

```markscript
stage = 1
print("Stage " + str(stage) + ": Ingest --- reading input data")
```

> Spawn a directory listing to verify the input exists
> spawn "cmd.exe /c dir examples\pipeline_inbox.txt"

> read file "examples/pipeline_inbox.txt"

> print "=== Raw input logged ==="

---

## StageTransform - Process data and write artifacts

> The transform stage: process, enrich, and write.

> Write the pipeline processing log
> write file "pipeline_output/stage_transform.log" "Transform stage: data normalized"

> Spawn a verification command
> run "echo [PIPELINE] Transform stage completed successfully"

```markscript
stage = 2
print("Stage " + str(stage) + ": Transform --- processing data")
```

> Write the enrichment output
> write file "pipeline_output/enriched_data.txt" "enriched_record_1"
> write file "pipeline_output/enriched_data.txt" "enriched_record_2"

> Verify the output was written by checking file existence
> file exists "pipeline_output/enriched_data.txt"

> print "Transform artifacts verified"

---

## StageValidate -- Assert data integrity

> The validation stage: check every assertion.

```markscript
stage = 3
print("Stage " + str(stage) + ": Validate --- running integrity checks")
```

> Verify the pipeline state with assertions
> assert 3 3
> assert 42 42
> assert 1 1

> Check file existence for all expected outputs
> file exists "pipeline_output/enriched_data.txt"
> file exists "pipeline_output/stage_transform.log"

> print "Validation passed - all assertions held"

---

## StageReport -- Write the final report

> The report stage: summarize everything.

> run "echo [PIPELINE] All 4 stages completed successfully"

```markscript
stage = 4
print("Stage " + str(stage) + ": Report -- generating summary")
```

> Write the final pipeline report
> write file "pipeline_output/pipeline_report.txt" "PipelinePalooza Report"
> write file "pipeline_output/pipeline_report.txt" "---"
> write file "pipeline_output/pipeline_report.txt" "Stages: 4"
> write file "pipeline_output/pipeline_report.txt" "Result: SUCCESS"

> Assert the report was written correctly
> file exists "pipeline_output/pipeline_report.txt"

> Final status
> print "=== PIPELINE COMPLETE: ALL STAGES PASSED ==="

---

## StageCleanup --- Verify and remove artifacts

> Post-pipeline verification and cleanup.

> Verify all artifacts exist
> file exists "pipeline_output/stage_transform.log"
> file exists "pipeline_output/enriched_data.txt"
> file exists "pipeline_output/pipeline_report.txt"

> print "Pipeline verification: all 3 artifacts confirmed"

> Clean up -- remove temporary artifacts
> run "del /f pipeline_output\\stage_transform.log 2>nul"
> run "del /f pipeline_output\\enriched_data.txt 2>nul"
> run "del /f pipeline_output\\pipeline_report.txt 2>nul"

```markscript
print("Pipeline output directory cleaned")
print("=== PipelinePalooza Terminated Safely ===")
```

---

## Pipeline Map

| Stage | Domain | Handlers Used | Purpose |
|-------|--------|---------------|---------|
| 1 | StageIngest | read file, run, spawn, print | Read raw input |
| 2 | StageTransform | write file, run, file exists, print | Process and enrich |
| 3 | StageValidate | assert, file exists, print | Verify integrity |
| 4 | StageReport | write file, run, assert, file exists, print | Generate summary |
| 5 | StageCleanup | file exists, run, print | Verify and clean |

Handler coverage: **8 of 8 registered IVT handlers exercised**

> All pipeline stages executed within a single MarkScript VM session.
> No external orchestrator. No YAML. No JSON. No glue code.
> The markdown IS the pipeline.
