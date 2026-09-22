# MKS Intent Keyword Registry
>
> Single source of truth for all MKS blockquote intent keywords.
> 
> To add a new intent: add a row to the table below.
> To change an intent's handler: edit the handler_fn column.
> No parser, compiler, or bridge modifications needed.
> 
> The parser reads this file at startup via registry.kn and uses
> the keyword column to decide whether a blockquote is an intent
> or prose documentation.

## Keywords

| keyword    | handler_fn               | handler_id | description               |
|------------|--------------------------|-----------|---------------------------|
| read       | handler_fs_read_text     | 2         | Read a file's content     |
| write      | handler_fs_write_text    | 3         | Write content to a file   |
| exists     | handler_fs_exists        | 3         | Check if a file exists    |
| import     | handler_import_kain      | 6         | Import a Kain module      |
| run        | handler_process_output   | 4         | Execute a command         |
| spawn      | handler_process_spawn    | 5         | Spawn a process           |
| assert     | handler_assert           | 7         | Assert two values equal   |
| print      | handler_println          | 8         | Print a value             |
| find       | handler_ui_get_widget    | 75        | Find a UI widget          |
| set        | handler_ui_set_property  | 76        | Set a UI widget property  |
| get        | handler_ui_get_property  | 77        | Get a UI widget property  |
| create     | handler_ui_create_widget | 78        | Create a UI widget        |
| concat     | handler_string_concat    | 13        | Concatenate strings       |
| split      | handler_string_split     | 14        | Split a string            |
| join       | handler_string_join      | 15        | Join strings              |
| substr     | handler_string_substr    | 16        | Extract substring         |
| replace    | handler_string_replace   | 17        | Replace in string         |
| upper      | handler_string_upper     | 18        | Uppercase a string        |
| lower      | handler_string_lower     | 19        | Lowercase a string        |
| trim       | handler_string_trim      | 20        | Trim whitespace           |
| contains   | handler_string_contains  | 21        | Check if string contains  |
| sin        | handler_math_sin         | 22        | Sine function             |
| cos        | handler_math_cos         | 23        | Cosine function           |
| sqrt       | handler_math_sqrt        | 24        | Square root               |
| abs        | handler_math_abs         | 25        | Absolute value            |
| min        | handler_math_min         | 26        | Minimum of two values     |
| max        | handler_math_max         | 27        | Maximum of two values     |
| clamp      | handler_math_clamp       | 28        | Clamp a value to range    |
| random     | handler_random_int_range | 49        | Random integer in range   |
| parse      | handler_json_parse       | 31        | Parse JSON string         |
| stringify  | handler_json_stringify   | 32        | Stringify to JSON         |
| mkdir      | handler_fs_mkdir         | 33        | Create a directory        |
| readdir    | handler_fs_read_dir      | 34        | Read directory listing    |
| stat       | handler_fs_stat          | 35        | Get file metadata         |
| touch      | handler_fs_touch         | 36        | Touch a file              |
| chmod      | handler_fs_chmod         | 37        | Change file permissions   |
| time       | handler_time_now         | 41        | Get current time          |
| sleep      | handler_time_sleep       | 42        | Sleep for milliseconds    |
| template   | handler_template_render  | 48        | Render a template         |
| randint    | handler_math_random_int  | 29        | Random integer            |
| randfloat  | handler_math_random_float| 30        | Random float              |
| randrange  | handler_random_int_range | 49        | Random int in range       |
| randfrange | handler_random_float_range| 50       | Random float in range     |
| maybe      | handler_math_random_int  | 29        | Random integer            |
| diceroll   | handler_random_int_range | 49        | Dice roll simulation      |
| await      | handler_process_await    | 52        | Await a process           |
| kill       | handler_process_kill_pid | 53        | Kill a process            |
| exitcode   | handler_process_exit_code| 54        | Get process exit code     |
| stdout     | handler_process_stdout   | 55        | Get process stdout        |
| stderr     | handler_process_stderr   | 56        | Get process stderr        |
| pipe       | handler_process_pipe     | 57        | Pipe data                 |
| env        | handler_process_env      | 58        | Get environment variable  |
| cwd        | handler_process_cwd      | 59        | Get current working dir   |
| click      | handler_ui_on_click      | 71        | Handle UI click           |
| key        | handler_ui_on_key        | 72        | Handle UI key             |
| focus      | handler_ui_on_focus      | 73        | Handle UI focus           |
| close      | handler_ui_on_close      | 74        | Handle UI close           |
| and        | handler_qualifier_echo   | 80        | Logical AND / concatenate |
| with       | handler_qualifier_echo   | 80        | Context / accompaniment   |
| exclude    | handler_qualifier_echo   | 80        | Filter / exclude items    |
| after      | handler_qualifier_echo   | 80        | Schedule after delay      |
| before     | handler_qualifier_echo   | 80        | Precondition gate         |
| from       | handler_qualifier_echo   | 80        | Source / extraction       |
| to         | handler_qualifier_echo   | 80        | Destination / conversion  |
| using      | handler_qualifier_echo   | 80        | Tool / method invocation  |
| by         | handler_qualifier_echo   | 80        | Group / sort / by-criteria|
| not        | handler_qualifier_echo   | 80        | Negation / logical NOT    |
| only       | handler_qualifier_echo   | 80        | Restrict / filter-only    |
| except     | handler_qualifier_echo   | 80        | Exception / exclusion     |
| until      | handler_qualifier_echo   | 80        | Loop until condition      |
| since      | handler_qualifier_echo   | 80        | Time since / from point   |
