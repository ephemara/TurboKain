# Intent Storm

> All 71 registered intent keywords in one file, chained pipelines, file
> roundtrips in tmp, JSON roundtrips, and deliberate error paths.
> File side effects stay in the OS tmp dir — never the repo.

## string_pipeline

> concat "hello" "world"
> upper "project genesis"
> lower "GOLDEN EXAMPLE"
> replace "hello world" "world" "mars"
> trim "   markscript   "
> contains "hello world" "world"
> split "a,b,c" ","
> join "-" "a" "b" "c"
> substr "hello world" 0 5

## math_pipeline

> sin 1.57
> cos 0.0
> sqrt 144
> abs -42
> min 7 3
> max 7 3
> clamp 15 0 10
> randint 1 100
> randfloat 0.0 1.0
> randrange 5 10

## json_roundtrip

> parse "{\"project\":\"genesis\",\"status\":\"live\"}"
> stringify "{\"a\":1}"

## template_render

> template "Project {{name}} — status: {{status}}"

## time_and_sleep

> time
> sleep 5
> time

## fs_roundtrip_tmp

> write "tmp_v2_storm.txt" "storm payload 123"
> read "tmp_v2_storm.txt"
> exists "tmp_v2_storm.txt"
> stat "tmp_v2_storm.txt"
> mkdir "tmp_v2_storm_dir"
> touch "tmp_v2_storm_dir/marker.txt"
> exists "tmp_v2_storm_dir/marker.txt"
> readdir "tmp_v2_storm_dir"

## assert_chain

```markscript
let sa = 6 * 7
let sb = sa + 0
```

> assert sa 42
> assert sb 42

## error_paths_graceful

> nosuchintent arg1 arg2
> print
> sqrt -1
> min 5

> print "INTENT STORM DONE"
