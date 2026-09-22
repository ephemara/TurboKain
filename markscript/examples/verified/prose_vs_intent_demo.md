# Prose vs Intent Disambiguation Demo

Tests the three-way classification of blockquotes:
1. Known intent keywords → dispatched to IVT handlers
2. Prose-starter words → treated as documentation (no bytecode)
3. Unknown words (not in either list) → treated as prose

The 50+ PROSE_STARTERS include articles, prepositions, pronouns,
conjunctions, interrogatives, and discourse markers.

---

## Category 1: Known Intent Keywords (Dispatched)

These first words ARE in the intent keyword registry:

> print "this is a known intent keyword"
> write ".mks_prose_test.txt" "prose test"
> read ".mks_prose_test.txt"
> concat "concat" "works"
> split "a,b" ","
> upper "upper works"
> lower "LOWER WORKS"
> trim "  trim works  "
> sin 0
> cos 0
> sqrt 9
> abs -10
> clamp 50 0 100

---

## Category 2: Prose-Starters (Documentation, NO dispatch)

These first words are in PROSE_STARTERS --- the parser recognizes
them and skips bytecode emission entirely:

### Articles & Determiners

> The quick brown fox jumps over the lazy dog.
> This is a documentation blockquote.
> That approach would be incorrect.
> These examples demonstrate the prose detection.
> Those values are ignored at compile time.
> A single blockquote can contain multiple sentences.
> An alternative design was considered.
> Some blockquotes are just documentation.
> Any word from the prose-starters list triggers this.
> All prose-starters are checked before intent dispatch.
> Each line here produces zero bytecode.
> Every parser pass includes this check.
> One important note about the architecture.
> No bytecode is emitted for these lines.
> Other words in the starters list behave identically.

### Pronouns

> I wrote this documentation blockquote.
> We considered several alternatives.
> You can add more examples here.
> He suggested using the data-driven approach.
> She documented the prose detection algorithm.
> It works exactly as specified.

### Prepositions

> In the parser code, prose detection happens first.
> At compile time, blockquotes are classified.
> On line 42, the keyword check occurs.
> By design, prose-starters never dispatch.
> From the beginning, this was the intended behavior.
> To add new prose-starters, edit the const array.
> With this design, documentation flows naturally.
> For every blockquote, we check the first word.

### Conjunctions

> And the detection works reliably.
> But edge cases must be tested.
> Or perhaps a different approach.
> If the first word is a prose-starter, we skip.
> Because the parser must be fast.
> However, we also check the registry.

### Interrogatives

> Who wrote this parser code?
> What happens with unknown words?
> When does the registry load?
> Where is the prose-starters list defined?
> Why do we need this disambiguation?
> Which words trigger the prose path?
> How does the three-way classification work?

### Discourse Markers

> Then the parser emits bytecode.
> Now we have a complete disambiguation system.
> Here is another prose example.
> There are over 50 prose-starter words.
> Still, some edge cases remain.
> Therefore, we test thoroughly.
> However, the design is sound.
> Meanwhile, the VM executes intents.
> Nevertheless, prose detection is reliable.
> Furthermore, the registry is data-driven.
> Moreover, new intents require zero parser changes.
> Thus, the system is maintainable.
> Hence, we recommend this approach.

---

## Category 3: Unknown Words (Prose, NO dispatch)

Words not in the registry and not prose-starters:

> marmalade is a delicious preserve made from citrus fruit.
> xylophone music filled the concert hall.
> quantum mechanics describes the behavior of subatomic particles.
> zephyr winds blew gently across the meadow.
> labyrinthine corridors twisted through the ancient castle.

---

## Verify

```markscript
print("prose_vs_intent_demo: all three categories exercised")
```
