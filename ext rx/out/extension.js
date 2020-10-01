"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = void 0;
// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
const vscode = require("vscode");
// this method is called when your extension is activated
// your extension is activated the very first time the command is executed
function activate(context) {
    // Use the console to output diagnostic information (console.log) and errors (console.error)
    // This line of code will only be executed once when your extension is activated
    console.log('RX Language extension has been successfully activated');
    // The command has been defined in the package.json file
    // Now provide the implementation of the command with registerCommand
    // The commandId parameter must match the command field in package.json
    let disposable = vscode.commands.registerCommand('extension.helloWorld', () => {
        // The code you place here will be executed every time your command is executed
        // Display a message box to the user
        vscode.window.showInformationMessage('RX Language extension has been successfully activated');
    });

	let ShowSelectedText = vscode.commands.registerCommand('extension.ShowSelectedText', () => {
		const editor = vscode.window.activeTextEditor;
		if (!editor){
			vscode.window.showErrorMessage('Editor Does not Exists');
			return
		}
        const text = editor.document.getText(editor.selection)
        if (!text){
			vscode.window.showErrorMessage('No Selected Word(s) Found');
			return
		}
		vscode.window.showInformationMessage('Selected Text:  '+text);
	});
	let terminal = vscode.commands.registerCommand('extension.terminal', () => {
        
        const x = vscode.window.activeTerminal;
        vscode.window.showInformationMessage(x);
	});

    context.subscriptions.push(disposable);
    context.subscriptions.push(ShowSelectedText);
    context.subscriptions.push(terminal);
}




exports.activate = activate;
// this method is called when your extension is deactivated
function deactivate() { }
exports.deactivate = deactivate;
//# sourceMappingURL=extension.js.map