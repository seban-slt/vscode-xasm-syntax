const vscode = require('vscode');

const TEMPLATE_FILES = ['tasks.json', 'launch.json', 'settings.json'];

/**
 * Select the workspace folder that should be initialized.
 *
 * @returns {Promise<vscode.WorkspaceFolder | undefined>}
 */
async function selectWorkspaceFolder() {
  const folders = vscode.workspace.workspaceFolders;

  if (!folders || folders.length === 0) {
    vscode.window.showErrorMessage(
      'XASM: Open a project folder before initializing the project.'
    );
    return undefined;
  }

  if (folders.length === 1) {
    return folders[0];
  }

  const selected = await vscode.window.showQuickPick(
    folders.map((folder) => ({
      label: folder.name,
      description: folder.uri.fsPath,
      folder
    })),
    {
      placeHolder: 'Select the workspace folder to initialize for XASM'
    }
  );

  return selected?.folder;
}

/**
 * Check whether a URI exists.
 *
 * @param {vscode.Uri} uri
 * @returns {Promise<boolean>}
 */
async function exists(uri) {
  try {
    await vscode.workspace.fs.stat(uri);
    return true;
  } catch (error) {
    if (error instanceof vscode.FileSystemError && error.code === 'FileNotFound') {
      return false;
    }
    throw error;
  }
}

/**
 * Initialize an XASM project in the selected workspace folder.
 * Existing VS Code configuration files are never overwritten.
 *
 * @param {vscode.ExtensionContext} context
 */
async function initializeProject(context) {
  const workspaceFolder = await selectWorkspaceFolder();
  if (!workspaceFolder) {
    return;
  }

  const vscodeDir = vscode.Uri.joinPath(workspaceFolder.uri, '.vscode');
  const templateDir = vscode.Uri.joinPath(
    context.extensionUri,
    'templates',
    'project',
    '.vscode'
  );

  try {
    await vscode.workspace.fs.createDirectory(vscodeDir);

    const created = [];
    const skipped = [];

    for (const fileName of TEMPLATE_FILES) {
      const source = vscode.Uri.joinPath(templateDir, fileName);
      const destination = vscode.Uri.joinPath(vscodeDir, fileName);

      if (await exists(destination)) {
        skipped.push(fileName);
        continue;
      }

      const content = await vscode.workspace.fs.readFile(source);
      await vscode.workspace.fs.writeFile(destination, content);
      created.push(fileName);
    }

    if (created.length === 0) {
      vscode.window.showInformationMessage(
        'XASM: Project is already initialized. Existing files were left unchanged.'
      );
      return;
    }

    let message = `XASM: Created ${created.map((name) => `.vscode/${name}`).join(', ')}.`;
    if (skipped.length > 0) {
      message += ` Existing ${skipped.map((name) => `.vscode/${name}`).join(', ')} left unchanged.`;
    }

    vscode.window.showInformationMessage(message);
  } catch (error) {
    const detail = error instanceof Error ? error.message : String(error);
    vscode.window.showErrorMessage(`XASM: Failed to initialize project: ${detail}`);
  }
}

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
  context.subscriptions.push(
    vscode.commands.registerCommand('xasm.initializeProject', () =>
      initializeProject(context)
    )
  );
}

function deactivate() {}

module.exports = {
  activate,
  deactivate
};
