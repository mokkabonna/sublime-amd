# Sublime AMD

__Under development, in early alpha__

If typing a undeclared variable in your AMD module, press ctrl+k, ctrk+i to automatically insert the module.

## Bugs
- Currently does not work unless you have already at least one module.
- Also works on only one the first module in the file (good practice anyway)
- Only works for define


The idea is to turn this:


    define(['jquery'], function($) {
      moment<== place cursor at end of word, then press ctrl+k, ctrk+i
    });


into this:

    define(['jquery', 'moment'], function($, moment, ) {
      moment
    });


You will be prompted to change the module name. The variable name is prefilled.
