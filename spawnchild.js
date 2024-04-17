const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

function createWindow() {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    win.loadFile('index.html');
}

ipcMain.on('fetch-data', (event, args) => {
    const pythonProcess = spawn('python3', ['path_to_your_script.py', args.auditYear]);
    let data = '';

    pythonProcess.stdout.on('data', (output) => {
        data += output;
    });

    pythonProcess.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
        event.sender.send('data-fetched', JSON.parse(data));
    });

    pythonProcess.stderr.on('data', (error) => {
        console.error(`stderr: ${error}`);
    });
});

app.whenReady().then(createWindow);
