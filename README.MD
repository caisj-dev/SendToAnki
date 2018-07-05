# sublime-sendtoAnki

> Sublime Text 3 plugin to send notes to Anki

This tool provide you with a convenient way to take notes and make Anki Cards. One of the biggest reasons many students love Anki is because of the powerful spaced repetition system.

<!-- 以下是动图链接 -->
<!-- <a href="https://www.patreon.com/sindresorhus">
    <img src="https://c5.patreon.com/external/logo/become_a_patron_button@2x.png" width="160">
</a> -->

---
<!-- 以下是动图说明 -->
<!-- ![](screenshot.gif) -->

---
<!-- 以下是功能描述，概要，罗列 -->


## Install
Note: this plugin hasn't been submitted to the [Package Control](https://packagecontrol.io) .
<!-- Install `Autoprefixer` with [Package Control](https://packagecontrol.io) and restart Sublime. -->
you should use sublime package manager
use cmd+shift+p then Package Control: Install Package
look for Confluence and install it.

### Dependency
#### Package Control Dependency
**Use the Package Control Satisefy Denpendency to Check, the dependency will be automatically installed**

#### Anki Dependency
**You need to have the following app installed:**
* [Anki](https://apps.ankiweb.net/) , Windows or Mac would be fine.
* [AnkiConnect](https://ankiweb.net/shared/info/2055492159),this is a Anki(decktop) plugin that provides API for external application to manipulate Anki's local database.

## Getting started
To get started, Please make sure to run Anki as well as  the plugin, AnkiConnect first.

### Creat New Note

Your notes are recommended to be taken in Markdown file, for the anki models are converted into an easy-to-read Markdown format.

In a Markdown file, open the Command Palette *(<kbd>ctrl</kbd> <kbd>;</kbd> )* and choose one of the Anki`deck` that you are going to place the note in. Then chose one of the model.

### Send to Anki
In a Markdown file, simply select all the notes that you would like to memorize. Right click at the select area and chose 'SendtoAnki' in the menu. Then each of the notes will be sent to specific deck in Anki, separately.


### Keyboard shortcut

You can also set up a keyboard shortcut to run the command by opening up "Preferences → Key Bindings - User" and adding your shortcut with the `insert_note_field_by_syntax` command.

Example:

```json
[
    {
        "keys": ["ctrl+\"],
        "command": "insert_note_field_by_syntax"
    }
]
```


## License

MIT © [Sindre Sorhus](https://sindresorhus.com)
