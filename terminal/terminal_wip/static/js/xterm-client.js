
var serverAddress = "";

createTerminal()

function createTerminal() {

    var input = "" // Current user input
    var saveInput = "" // Retain user input when using up/down arrow keys
    var inputHistory = [] // History of past inputs
    var historyIndex = 0 // Used to iterate through input history
    var cursorIndex = 0 // Where the cursor should be relative to input
    var post = "" // Segment of current user input located behind cursor

    // Initiate terminal
    var term = new Terminal({cursorBlink: true, cursorStyle: "bar"})
    term.open(document.getElementById('terminal'))
    term.writeln(" Welcome to Private")

    var prompt = ' > ';
    term.prompt = function () {
        term.write('\r\n' + prompt)
        input = ""
    };
    term.prompt()

    // ---------------- Needs to send and receive data via ajax ----------------- //

    // Don't really need this function
    // as term.writeln does the same thing
    term.write_response = function(res) {
        term.writeln(res)
    }

    term.send_cmd = function(cmd) {
        if (!cmd) return;

        //write_cmd(cmd);
        data = { 'cmd': cmd, 'uid': '1234567' };

        $.ajax({
            type: "POST",
            url: 'http://localhost:5000/analyze',
            data: data,
            success: function(data){
                console.log(data);
                if(data.response){
                    //term.write_response(data.response)
                    term.writeln(data.response);
                }
            },
            dataType: "json"
        });
    }

    term.enter = function () {
        // Enter key has been pressed


        var cmd = $.trim(input);
        term.send_cmd(cmd);
        $("#cmd").val("");

        callback() ;
    }

    callback = function() {
        // Call this function after ajax processes are complete

        // Save the input
        if (input != inputHistory[inputHistory.length - 1]) {
            // Don't want to save the same command twice
            inputHistory.push(input)
        }

        // Reset counts
        historyIndex = inputHistory.length
        cursorIndex = 0
        post = ""

        // Start a new line
        term.prompt()
    }

    // -------------------------------------------------------------------------- //

    term.deleteLine = function () {
        // Deletes all of the text (asides from the prompt) on the current
        // line

        while (cursorIndex < input.length + 1) {
            // Make sure we're at the end of the line
            term.bringCursorForwards(1)
            cursorIndex += 1
        }
        while (input.length > 0) {
            term.write('\b \b')
            input = input.slice(0, -1)
        }
        cursorIndex = 0
    }

    term.bringCursorBackwards = function (n) {
        // Brings the cursor backwards by n
        for (var i = 0; i < n; i++) {
            term.write('\x1b[D')
        }
    }

    term.bringCursorForwards = function (n) {
        // Brings the cursor forward by n
        for (var i = 0; i < n; i++) {
            term.write('\x1b[C')
        }
    }

    term.on('paste', function (data, ev) {

        // Save the stuff before and after the position at which we're
        // pasting
        pre = input.slice(0, cursorIndex)
        pki = cursorIndex

        // Clear the line
        term.deleteLine()
        term.write('\b \b')

        // Write the new user input
        input = pre + data + post
        term.write(input)

        // Bring the cursor back to where it should be after pasting
        term.bringCursorBackwards(post.length)
        cursorIndex = pre.length + data.length
    });

    term.on('key', function (key, ev) {

        var printable = (
            !ev.altKey && !ev.altGraphKey && !ev.ctrlKey && !ev.metaKey
        );

        if (ev.key == 'Enter') {
            // enter
            term.enter()

        } else if (ev.key == 'Backspace') {
            // backspace
            if (input.slice(0, cursorIndex).length > 0) {
                // So we don't delete the prompt
                term.write('\b \b')

                if (post.length == 0) {
                    // Cursor is at the end of the line, simply cut down
                    input = input.slice(0, -1)
                    post = ""
                } else {
                    // We need to move post back

                    // Save the stuff from before the cursor
                    pre = input.slice(0, cursorIndex - 1)
                    tki = cursorIndex

                    // Clear the line
                    term.deleteLine()
                    cursorIndex = tki

                    // Write the new input, with post being pushed back by one
                    input = pre + post
                    term.write(input)
                    term.bringCursorBackwards(post.length)
                    post = input.slice(cursorIndex-1)
                }
                cursorIndex -= 1
            }

        } else if (ev.key == 'ArrowLeft') {
            // Left arrow key
            if (cursorIndex > 0) {
                cursorIndex -= 1
                term.bringCursorBackwards(1)
                post = input.slice(cursorIndex)
            }

        } else if (ev.key == 'ArrowRight') {
            // Right arrow key
            if (cursorIndex < input.length) {
                cursorIndex += 1
                term.bringCursorForwards(1)
                post = input.slice(cursorIndex)
            }

        } else if (ev.key == 'ArrowUp'){
            // Up arrow key - go backwards in input command history
            ev.preventDefault()
            if (historyIndex == inputHistory.length) {
                // User is moving from their current input into past inputs -
                // save what they've currently written
                saveInput = input
            }

            if (historyIndex >= 0 && inputHistory.length > 0) {
                if (historyIndex != 0) {
                    historyIndex -= 1
                }

                // Clear the line
                term.deleteLine()
                term.write('\b \b')

                // Write the previous input
                input = inputHistory[historyIndex]
                term.write(input)
                cursorIndex = input.length
            }

        } else if (ev.key == 'ArrowDown') {
            // Down arrow key - go forwards in input command history
            ev.preventDefault()
            if (historyIndex < inputHistory.length - 1) {
                historyIndex += 1

                // Clear the line
                term.deleteLine()
                term.write('\b \b')

                // Write the next input
                input = inputHistory[historyIndex]
                term.write(input)
                cursorIndex = input.length

            } else if (historyIndex == inputHistory.length - 1) {
                // User has come back to (what was) their current input
                historyIndex += 1

                // Clear the line
                term.deleteLine()
                term.write('\b \b')

                // Rewrite their old current input
                input = saveInput
                term.write(input)
                cursorIndex = input.length
            }

        } else if (ev.key == 'Tab') {
            // Tab - 4 spaces to make backspaces easier
            ev.preventDefault()
            input += "    "
            term.write("    ")
            cursorIndex += 4

        } else if (printable) {
            // regular input
            if (post.length > 0) {
                // We have to re-position post, or else we'll write over it

                // Save the stuff that we want to keep
                pre = input.slice(0, cursorIndex)
                pki = cursorIndex

                // Clear the line
                term.deleteLine()
                term.write('\b \b')

                // Write down the new input
                input = pre + key + post
                term.write(input)
                term.bringCursorBackwards(post.length)
                cursorIndex = pki
            } else {
                input += key
                term.write(key);
            }
            cursorIndex += 1
        }
    });
};
