"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = void 0;

const vscode = require("vscode");
const path = require("path");

















// {!!!}
function followEditorChange() {
    if (vscode.workspace.getConfiguration("terminalSync").get("followActiveEditor", false)) {
        changeDirectory();
    }
}










// Run RX File
async function run(dbug=0){
    //vscode.window.showInformationMessage('RX Language extension has been successfully activated');
    
    let editor = vscode.window.activeTextEditor;
    if (editor && !editor.document.isUntitled) {editor.document.save();}
    
    var terminal_run = vscode.window.activeTerminal;
    if (terminal_run){
        await changeDirectory();
    }
    else{
        create_terminal_currentdir();
        await sleep(2000);
    }
    terminal_run = vscode.window.activeTerminal;
    if (editor && !editor.document.isUntitled){
        //let FN = path.basename(editor.document.fileName);
        switch (dbug) {
            case 0:
                terminal_run.sendText(`RX ${path.basename(editor.document.fileName)}`,true);
                break;
        
            case 1:
                terminal_run.sendText(`RX ${path.basename(editor.document.fileName)} -d`,true);
                break;
    
            case 2:
                terminal_run.sendText(`RX ${path.basename(editor.document.fileName)} --debug`,true);
                break;
        }
    }
    else {
        terminal_run.sendText(`RX`,true);  //"\x03"
    }
}
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
function changeDirectory() {
    var editor = vscode.window.activeTextEditor
    var terminal_chdir = vscode.window.activeTerminal;
    var _a, _b;
    let uri = (_b = (_a = vscode.window.activeTextEditor) === null || _a === void 0 ? void 0 : _a.document) === null || _b === void 0 ? void 0 : _b.uri;
    if (uri && terminal_chdir && editor && !editor.document.isUntitled) {
        
        if (terminal_chdir.name == 'python'){
            terminal_chdir.sendText(`\x1A`,true); 
        }
        else {
            terminal_chdir.sendText(`\x03`);
        }
        terminal_chdir.sendText(`${path.dirname(uri.fsPath).slice(0,2)}`, true);
        terminal_chdir.sendText(`cd "${path.dirname(uri.fsPath)}"`, true);
        
        //vscode.commands.executeCommand('workbench.action.terminal.sendSequence',{"text":"cd \"${fileDirname}\"\u000D"});
    }
}
function create_terminal_currentdir(){
    var terminal_createterminal = vscode.window.activeTerminal;
    if (!terminal_createterminal){
        var editor = vscode.window.activeTextEditor;
        if (editor && !editor.document.isUntitled){
            var FN = path.dirname(editor.document.fileName); //.uri.fsPath
        }
        else {var FN = 'C:\\'}
        
        terminal_createterminal = vscode.window.createTerminal( {cwd:FN} );
        terminal_createterminal.show(false);
        
        vscode.commands.executeCommand('workbench.action.terminal.newWithCwd',{ "cwd": "${fileDirname}" });
    }
}
var Run = vscode.commands.registerCommand('extension.run', run)

// Debuggers
function debug(){ run(1) }
let Debug = vscode.commands.registerCommand('extension.debug', debug);
function debug_only(){ run(2) }
let Debug_Only = vscode.commands.registerCommand('extension.debugonly', debug_only);



// Show Selected Text
function show_selected_text() {
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
};
var ShowSelectedText = vscode.commands.registerCommand('extension.ShowSelectedText', show_selected_text)






// {USEFULL}
/*
var editor = vscode.window.activeTextEditor
//] ACTIVE FILE
editor.document.fileName                // Abspath
editor.document.getText()               // Content
editor.document.isUntitled              // Abspath
editor.document.languageId              // Language ID
editor.document.lineAt(3).text          // Get Text of line 3+1 (index 3)
editor.document.lineCount.toString()    // Line Numbers
editor.viewColumn.toString()            // In which Column
*/






















function activate(context) {
    console.log('RX Language extension has been successfully activated');
    





    function Test(){
        var t = vscode.window.activeTerminal;
        //vscode.window.showErrorMessage(t.name);
        vscode.commands.executeCommand('workbench.action.terminal.sendSequence',{"text":"cd /d \"${fileDirname}\"\u000D"})
    }
    let TEST = vscode.commands.registerCommand('extension.TEST', Test);
    context.subscriptions.push(TEST);


    context.subscriptions.push(Run);
    context.subscriptions.push(Debug);
    context.subscriptions.push(Debug_Only);



}




















exports.activate = activate;
// this method is called when your extension is deactivated
function deactivate() { }
exports.deactivate = deactivate;
//# sourceMappingURL=extension.js.map