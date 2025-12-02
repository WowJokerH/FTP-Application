from PyQt6 import QtCore, QtGui, QtWidgets
import threading
import datetime
from clientInterface import Ui_MainWindow
from ftpClient import FTPclient
import sys
import os
import socket

# Windows taskbar icon fix
try:
    from ctypes import windll
    myappid = 'wjh.ftpclient.app.1.0'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except:
    pass

class cleintInterface(QtCore.QObject, Ui_MainWindow):

    def applyStyles(self):
        style_sheet = """
        QMainWindow {
            background-color: #f0f2f5;
            font-family: "Segoe UI", "Microsoft YaHei", sans-serif;
            font-size: 9pt;
            color: #333333;
        }
        
        /* Status Panel Container */
        QWidget#statusPanel {
            background-color: #ffffff;
            border: 1px solid #dcdfe6;
            border-radius: 4px;
            margin: 5px 0px;
        }
        
        /* Labels */
        QLabel {
            color: #606266;
        }
        QLabel#connectionStatusLabel {
            font-weight: bold;
            color: #409EFF;
        }

        /* Input Fields */
        QLineEdit {
            padding: 5px 8px;
            border: 1px solid #dcdfe6;
            border-radius: 4px;
            background-color: #ffffff;
            color: #606266;
        }
        QLineEdit:focus {
            border: 1px solid #409EFF;
        }
        QLineEdit:read-only {
            background-color: #f5f7fa;
            color: #909399;
        }

        /* ComboBox */
        QComboBox {
            padding: 5px 8px;
            border: 1px solid #dcdfe6;
            border-radius: 4px;
            background-color: #ffffff;
            color: #606266;
        }
        QComboBox:hover {
            border-color: #c0c4cc;
        }
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 25px;
            border-left-width: 0px;
        }

        /* Buttons */
        QPushButton {
            background-color: #ffffff;
            border: 1px solid #dcdfe6;
            border-radius: 4px;
            padding: 6px 15px;
            color: #606266;
        }
        QPushButton:hover {
            color: #409EFF;
            border-color: #c6e2ff;
            background-color: #ecf5ff;
        }
        QPushButton:pressed {
            color: #3a8ee6;
            border-color: #3a8ee6;
        }
        
        /* Primary Button (Login) */
        QPushButton#loginButton {
            background-color: #409EFF;
            border-color: #409EFF;
            color: #ffffff;
        }
        QPushButton#loginButton:hover {
            background-color: #66b1ff;
            border-color: #66b1ff;
        }
        QPushButton#loginButton:pressed {
            background-color: #3a8ee6;
            border-color: #3a8ee6;
        }

        /* Danger Button (Logout) */
        QPushButton#logoutButton {
            background-color: #F56C6C;
            border-color: #F56C6C;
            color: #ffffff;
        }
        QPushButton#logoutButton:hover {
            background-color: #f78989;
            border-color: #f78989;
        }
        QPushButton#logoutButton:pressed {
            background-color: #dd6161;
            border-color: #dd6161;
        }

        /* Trees and Tables */
        QTreeView, QTableView, QTreeWidget, QTableWidget {
            background-color: #ffffff;
            border: 1px solid #dcdfe6;
            border-radius: 4px;
            gridline-color: #ebeef5;
            selection-background-color: #ecf5ff;
            selection-color: #409EFF;
            outline: none;
        }
        QHeaderView::section {
            background-color: #f5f7fa;
            padding: 8px;
            border: none;
            border-bottom: 1px solid #ebeef5;
            border-right: 1px solid #ebeef5;
            font-weight: bold;
            color: #909399;
        }
        QTableCornerButton::section {
            background-color: #f5f7fa;
            border: none;
        }

        /* Splitter */
        QSplitter::handle {
            background-color: #dcdfe6;
        }
        QSplitter::handle:horizontal {
            width: 1px;
        }
        QSplitter::handle:vertical {
            height: 1px;
        }
        
        /* Scrollbars */
        QScrollBar:vertical {
            background: #f5f7fa;
            width: 12px;
            margin: 0px;
        }
        QScrollBar::handle:vertical {
            background: #c0c4cc;
            min-height: 20px;
            border-radius: 6px;
            margin: 2px;
        }
        QScrollBar::handle:vertical:hover {
            background: #909399;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        QScrollBar:horizontal {
            background: #f5f7fa;
            height: 12px;
            margin: 0px;
        }
        QScrollBar::handle:horizontal {
            background: #c0c4cc;
            min-width: 20px;
            border-radius: 6px;
            margin: 2px;
        }
        QScrollBar::handle:horizontal:hover {
            background: #909399;
        }
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
            width: 0px;
        }

        /* Tab Widget */
        QTabWidget::pane {
            border: 1px solid #dcdfe6;
            border-radius: 4px;
            top: -1px;
            background-color: #ffffff;
        }
        QTabBar::tab {
            background: #f5f7fa;
            border: 1px solid #dcdfe6;
            padding: 8px 20px;
            margin-right: 2px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            color: #909399;
        }
        QTabBar::tab:selected {
            background: #ffffff;
            border-bottom-color: #ffffff;
            color: #409EFF;
            font-weight: bold;
        }
        QTabBar::tab:hover {
            color: #409EFF;
        }

        /* Progress Bar */
        QProgressBar {
            border: none;
            border-radius: 5px;
            text-align: center;
            background-color: #ebeef5;
        }
        QProgressBar::chunk {
            background-color: #67C23A;
            border-radius: 5px;
        }
        
        /* Log Window (Dark Theme) */
        QTableWidget#statusWindow {
            background-color: #2b2b2b;
            color: #f0f0f0;
            font-family: "Consolas", monospace;
            border: 1px solid #444;
        }
        QTableWidget#statusWindow QHeaderView::section {
            background-color: #333;
            color: #ddd;
            border-bottom: 1px solid #555;
        }
        """
        self.centralwidget.setStyleSheet(style_sheet)
        self.localdir.setAlternatingRowColors(True)
        self.remotedir.setAlternatingRowColors(True)
        
        # Setup status window (FTP command log)
        self.statusWindow.setColumnCount(1)
        self.statusWindow.setHorizontalHeaderLabels(["FTP 命令日志"])
        self.statusWindow.horizontalHeader().setStretchLastSection(True)
        self.statusWindow.verticalHeader().setVisible(False)
        self.statusWindow.setShowGrid(False)

    def __init__(self, ftpClientUI, ftpLogic):
        
        QtCore.QObject.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(ftpClientUI)
        self.applyStyles()
        self.ftpLogic = ftpLogic
        
        # Connect Signals
        self.loginButton.clicked.connect(self.loginButtonClicked)
        self.logoutButton.clicked.connect(self.logoutButtonClicked)
        
        # State variables
        self.numFiles = 0
        self.finerList = []
        self.currentRemotePath = '/'
        self.remoteTreeItems = {} # Map path to QTreeWidgetItem
        
        # Transfer queue management
        self.transferQueue = []  # List of transfer tasks
        self.transferLock = threading.Lock()
        self.isTransferring = False
        
        # Setup progress callback
        self.ftpLogic.progress_callback = self.updateTransferProgress
        
        # Initialize queue tables
        self.queueTable.setAlternatingRowColors(True)
        self.failedTable.setAlternatingRowColors(True)
        self.successTable.setAlternatingRowColors(True)
        
        # Update connection status
        self.updateConnectionStatus("未连接")
        
        # --- Local File System Setup ---
        self.currentLocalPath = QtCore.QDir.currentPath()
        self.clientDirectory = QtGui.QStandardItemModel()
        self.clientDirectory.setHorizontalHeaderLabels(["文件名", "大小", "类型", "修改时间"])
        
        self.localdir.setModel(self.clientDirectory)
        self.localdir.setRootIsDecorated(False)
        self.localdir.setSortingEnabled(True)
        self.localdir.header().resizeSection(0, 200)
        
        self.refreshLocalView(self.currentLocalPath)
        
        # Populate Local Path ComboBox with Drives
        self.populateLocalDrives()
        self.localPath.currentIndexChanged.connect(self.changeLocalRoot)
        self.localdir.doubleClicked.connect(self.localDirDoubleClicked)
        
        # --- Remote File System Setup ---
        # Remote Tree (Folders only)
        self.remoteTree.setHeaderLabel("远程目录结构")
        self.remoteTree.itemClicked.connect(self.remoteTreeItemClicked)
        self.remoteTree.itemExpanded.connect(self.remoteTreeItemExpanded)
        
        # Remote Table (Files and Folders)
        self.remotedir.setColumnCount(6)
        self.remotedir.setHorizontalHeaderLabels(["文件名", "文件类型", "文件大小", "最近修改", "权限", "所有者/组"])
        self.remotedir.cellDoubleClicked.connect(self.remoteTableDoubleClicked)
        
        # Enable Drag and Drop
        self.setupDragAndDrop()
        
        # Context Menus
        self.setupContextMenus()

    def refreshLocalView(self, path):
        self.clientDirectory.removeRows(0, self.clientDirectory.rowCount())
        self.currentLocalPath = path
        
        # Update Combo Box Text
        self.localPath.blockSignals(True)
        if self.localPath.findText(path) == -1:
            self.localPath.addItem(path)
        self.localPath.setCurrentText(path)
        self.localPath.blockSignals(False)
        
        # Add ".."
        is_root = False
        if sys.platform == 'win32':
            if len(path) <= 3 and ':' in path:
                is_root = True
        else:
            if path == '/':
                is_root = True
                
        if not is_root:
            item_name = QtGui.QStandardItem("..")
            item_name.setIcon(QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_DirIcon))
            item_name.setData("..", QtCore.Qt.ItemDataRole.UserRole) 
            self.clientDirectory.appendRow([item_name, QtGui.QStandardItem(""), QtGui.QStandardItem(""), QtGui.QStandardItem("")])

        # List files
        try:
            d = QtCore.QDir(path)
            d.setFilter(QtCore.QDir.Filter.AllEntries | QtCore.QDir.Filter.Hidden | QtCore.QDir.Filter.System | QtCore.QDir.Filter.NoDotAndDotDot)
            d.setSorting(QtCore.QDir.SortFlag.Name | QtCore.QDir.SortFlag.DirsFirst)
            
            file_infos = d.entryInfoList()
            icon_provider = QtWidgets.QFileIconProvider()
            
            for fi in file_infos:
                name = fi.fileName()
                size = str(fi.size()) if fi.isFile() else ""
                type_ = "文件夹" if fi.isDir() else "文件"
                date = fi.lastModified().toString("yyyy-MM-dd HH:mm:ss")
                
                item_name = QtGui.QStandardItem(name)
                item_name.setIcon(icon_provider.icon(fi))
                item_name.setData(fi.absoluteFilePath(), QtCore.Qt.ItemDataRole.UserRole)
                
                item_size = QtGui.QStandardItem(size)
                item_type = QtGui.QStandardItem(type_)
                item_date = QtGui.QStandardItem(date)
                
                self.clientDirectory.appendRow([item_name, item_size, item_type, item_date])
                
        except Exception as e:
            print(f"Error listing local files: {e}")

    def populateLocalDrives(self):
        self.localPath.clear()
        drives = QtCore.QDir.drives()
        for drive in drives:
            self.localPath.addItem(drive.absoluteFilePath())
        
        self.localPath.setCurrentText(self.currentLocalPath)

    def changeLocalRoot(self):
        path = self.localPath.currentText()
        if os.path.exists(path):
            self.refreshLocalView(path)

    def localDirDoubleClicked(self, index):
        path_data = index.data(QtCore.Qt.ItemDataRole.UserRole)
        
        if path_data == "..":
            parent_dir = os.path.dirname(self.currentLocalPath)
            self.refreshLocalView(parent_dir)
            return
            
        if not path_data: return
        
        if os.path.isdir(path_data):
            self.refreshLocalView(path_data)
        else:
            QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(path_data))

    def setupDragAndDrop(self):
        # Local
        self.localdir.setDragEnabled(True)
        self.localdir.setAcceptDrops(True)
        self.localdir.setDragDropMode(QtWidgets.QAbstractItemView.DragDropMode.DragDrop)
        self.localdir.setDefaultDropAction(QtCore.Qt.DropAction.CopyAction)
        
        # Patch Local Drag/Drop
        self.localdir.dragEnterEvent = self.localDragEnterEvent
        self.localdir.dragMoveEvent = self.localDragMoveEvent
        self.localdir.dropEvent = self.localDropEvent
        self.localdir.startDrag = self.localStartDrag
        
        # Remote
        self.remotedir.setDragEnabled(True)
        self.remotedir.setAcceptDrops(True)
        self.remotedir.setDragDropMode(QtWidgets.QAbstractItemView.DragDropMode.DragDrop)
        self.remotedir.setDefaultDropAction(QtCore.Qt.DropAction.CopyAction)
        
        # Patch Remote Drag/Drop
        self.remotedir.dragEnterEvent = self.remoteDragEnterEvent
        self.remotedir.dragMoveEvent = self.remoteDragMoveEvent
        self.remotedir.dropEvent = self.remoteDropEvent
        self.remotedir.startDrag = self.remoteStartDrag

    def setupContextMenus(self):
        self.localdir.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.localdir.customContextMenuRequested.connect(self.showLocalContextMenu)
        
        self.remotedir.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.remotedir.customContextMenuRequested.connect(self.showRemoteContextMenu)

    # --- Login / Logout ---
    def loginButtonClicked(self):
        try:
            self.updateConnectionStatus("正在连接...")
            self.ftpLogic.initConnection(self.hostname.text(), int(self.port.text()))
            self.ftpLogic.login(self.username.text(), self.password.text())
            self.statusMSG()
            self.ftpLogic.setMode('I')
            self.localdir.setEnabled(True)
            
            # Reset remote path states
            self.ftpLogic.pwd = '/'
            self.currentRemotePath = '/'
            
            self.ftpLogic.startPassiveDTPconnection()
            self.ftpLogic.getList()
            
            # Initialize Remote Tree Root
            self.remoteTree.clear()
            self.remoteTreeItems = {}
            rootItem = QtWidgets.QTreeWidgetItem(self.remoteTree, ["/"])
            rootItem.setData(0, QtCore.Qt.ItemDataRole.UserRole, "/")
            self.remoteTreeItems["/"] = rootItem
            
            # Load root directory content
            self.refreshRemoteView()
            self.remoteTree.expandItem(rootItem)
            
            # Update status
            self.updateConnectionStatus(f"已连接到 {self.hostname.text()}:{self.port.text()}")
            self.updateTransferStatus("空闲")
            
        except Exception as e:
            self.updateConnectionStatus(f"连接失败: {str(e)}")

    def logoutButtonClicked(self):
        try:
            self.ftpLogic.logout()
            self.statusMSG()
            self.remotedir.setRowCount(0)
            self.remoteTree.clear()
            self.remotePath.clear()
            # Reset states
            self.currentRemotePath = '/'
            self.remoteTreeItems = {}
            self.finerList.clear()
            
            # Update status
            self.updateConnectionStatus("未连接")
            self.updateTransferStatus("空闲")
            self.currentTransferLabel.setText("")
            self.transferProgressBar.setValue(0)
        except:
            pass

    # --- Remote Navigation Logic ---
    @QtCore.pyqtSlot()
    def _parseDirectoryData(self, dir_list):
        """Parse raw directory list into structured format.
        Returns: (parsed_items, file_count, dir_count, total_size)
        """
        parsed_items = []
        total_size = 0
        file_count = 0
        dir_count = 0

        for element in dir_list:
            if not element.strip():
                continue
            
            # Server uses tabs as delimiters, split by tab
            temp = element.split('\t')
            
            if len(temp) >= 6:
                perms = temp[0].strip()
                links_user = temp[1].strip().split()
                links = links_user[0] if links_user else '1'
                
                group = temp[2].strip()
                size = temp[4].strip()
                date_parts = temp[5].strip().split()
                
                if len(date_parts) >= 3:
                    month = date_parts[0]
                    day = date_parts[1]
                    time_or_year = date_parts[2]
                else:
                    month = day = time_or_year = ""
                
                filename = temp[6].strip() if len(temp) > 6 else ""
                
                # Build parsed item: [perms, links, owner, group, size, month, day, time, filename]
                item_data = [perms, links, 'user', group, size, month, day, time_or_year, filename]
                parsed_items.append(item_data)
                
                if perms.startswith('d'):
                    dir_count += 1
                else:
                    file_count += 1
                    try:
                        total_size += int(size)
                    except:
                        pass
        
        return parsed_items, file_count, dir_count, total_size
    
    def refreshRemoteView(self):
        """Refresh both tree and table views - used after login or major operations."""
        self.refreshRemoteTable()
        # Also update tree structure
        self._updateRemoteTree()
    
    def refreshRemoteTable(self):
        """Refresh only the table view without touching the tree - used when navigating via tree."""
        self.remotedir.setRowCount(0)
        self.finerList.clear()
        self.dirList = self.ftpLogic.returnDirList()
        
        # Update current path display
        self.currentRemotePath = self.ftpLogic.pwd
        self.remotePath.setText(self.currentRemotePath)
        
        # Parse directory data
        parsed_items, file_count, dir_count, total_size = self._parseDirectoryData(self.dirList)
        
        # Sort items: directories first, then files, alphabetically within each group
        def sort_key(item):
            if len(item) < 9:
                return (1, '')  # Invalid items go last
            name = item[8]
            perms = item[0]
            is_dir = perms.startswith('d')
            # Return tuple: (0 for dirs, 1 for files, lowercase name for case-insensitive sort)
            return (0 if is_dir else 1, name.lower())
        
        parsed_items.sort(key=sort_key)
        
        self.finerList = parsed_items
        self.numFiles = len(self.finerList)
        
        # Update Status in transfer status label
        status_text = f"{file_count} 个文件 和 {dir_count} 个目录。大小总计: {total_size:,} 字节"
        # We can show this in the statusbar or just skip it for now
        
        # 1. Update Table (Files AND Folders)
        # Add ".." if not root
        start_row = 0
        if self.currentRemotePath != '/':
            self.remotedir.setRowCount(self.numFiles + 1)
            
            item_dot = QtWidgets.QTableWidgetItem("..")
            item_dot.setIcon(QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_DirIcon))
            self.remotedir.setItem(0, 0, item_dot)
            self.remotedir.setItem(0, 1, QtWidgets.QTableWidgetItem("文件夹"))
            self.remotedir.setItem(0, 2, QtWidgets.QTableWidgetItem(""))
            self.remotedir.setItem(0, 3, QtWidgets.QTableWidgetItem(""))
            self.remotedir.setItem(0, 4, QtWidgets.QTableWidgetItem("drwxrwxrwx"))
            self.remotedir.setItem(0, 5, QtWidgets.QTableWidgetItem(""))
            start_row = 1
        else:
            self.remotedir.setRowCount(self.numFiles)
        
        # Process each item for table only
        for row, items in enumerate(self.finerList):
            try:
                # items: [perms, links, owner, group, size, month, day, time, name]
                if len(items) < 9:
                    continue
                    
                name = items[8]
                perms = items[0]
                is_dir = perms.startswith('d')
                size = items[4]
                date_str = f"{items[5]} {items[6]} {items[7]}"
                owner_group = f"{items[2]} {items[3]}"
                
                # Type
                if is_dir:
                    file_type = "文件夹"
                else:
                    ext = os.path.splitext(name)[1].upper()
                    if ext:
                        file_type = f"{ext[1:]} 文件"
                    else:
                        file_type = "文件"

                # Size formatting
                try:
                    size_int = int(size)
                    size_str = f"{size_int:,}"
                except:
                    size_str = size
                
                # Update Table
                table_row = start_row + row
                
                item_name = QtWidgets.QTableWidgetItem(name)
                if is_dir:
                    item_name.setIcon(QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_DirIcon))
                else:
                    item_name.setIcon(QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_FileIcon))
                
                self.remotedir.setItem(table_row, 0, item_name)
                self.remotedir.setItem(table_row, 1, QtWidgets.QTableWidgetItem(file_type))
                self.remotedir.setItem(table_row, 2, QtWidgets.QTableWidgetItem(size_str))
                self.remotedir.setItem(table_row, 3, QtWidgets.QTableWidgetItem(date_str))
                self.remotedir.setItem(table_row, 4, QtWidgets.QTableWidgetItem(perms))
                self.remotedir.setItem(table_row, 5, QtWidgets.QTableWidgetItem(owner_group))
                    
            except Exception as e:
                continue
        
        self.statusMSG()
        self.generateLogTable()
    
    def _updateRemoteTree(self):
        """Update tree structure with folders from current directory."""
        # Get current tree item
        current_tree_item = self.remoteTreeItems.get(self.currentRemotePath)
        if not current_tree_item:
            # Create missing path nodes
            current_tree_item = self._createPathNodes(self.currentRemotePath)
        
        # Clear existing children to avoid stale nodes after deletion
        self._clearTreeChildren(current_tree_item)
        
        # Add folder children to current node
        self._addTreeChildren(current_tree_item, self.currentRemotePath, self.finerList)

    def _clearTreeChildren(self, parent_item):
        """Clear all children of a tree item and update remoteTreeItems dict."""
        # Get all children from the tree item directly
        children = []
        for i in range(parent_item.childCount()):
            child = parent_item.child(i)
            if child:
                children.append(child)
        
        # Recursively collect all paths to remove
        paths_to_remove = []
        for child in children:
            child_path = child.data(0, QtCore.Qt.ItemDataRole.UserRole)
            if child_path:
                # Remove this child and all its descendants
                self._removeTreeItemRecursively(child, paths_to_remove)
        
        # Remove from dict
        for path in paths_to_remove:
            if path in self.remoteTreeItems:
                del self.remoteTreeItems[path]
        
        # Remove all children from tree
        parent_item.takeChildren()
    
    def _removeTreeItemRecursively(self, item, paths_to_remove):
        """Recursively collect paths of an item and all its descendants."""
        item_path = item.data(0, QtCore.Qt.ItemDataRole.UserRole)
        if item_path:
            paths_to_remove.append(item_path)
        
        # Recursively process children
        for i in range(item.childCount()):
            child = item.child(i)
            if child:
                self._removeTreeItemRecursively(child, paths_to_remove)
    
    def _createPathNodes(self, path):
        """Create all parent nodes for a given path if they don't exist."""
        if path == '/':
            return self.remoteTreeItems.get('/')
        
        # Split path into components
        parts = [p for p in path.split('/') if p]
        current_path = '/'
        parent_item = self.remoteTreeItems.get('/')
        
        for part in parts:
            current_path = current_path.rstrip('/') + '/' + part
            
            if current_path not in self.remoteTreeItems:
                # Create new tree item
                new_item = QtWidgets.QTreeWidgetItem(parent_item, [part])
                new_item.setData(0, QtCore.Qt.ItemDataRole.UserRole, current_path)
                self.remoteTreeItems[current_path] = new_item
                # Add dummy child to show expand arrow
                dummy = QtWidgets.QTreeWidgetItem(new_item, [""])
                new_item.setData(0, QtCore.Qt.ItemDataRole.UserRole + 1, True)
                parent_item = new_item
            else:
                parent_item = self.remoteTreeItems[current_path]
        
        return parent_item

    def _addTreeChildren(self, parent_item, parent_path, parsed_items):
        """Add folder children to a tree item.
        Args:
            parent_item: QTreeWidgetItem to add children to
            parent_path: Full path of parent directory
            parsed_items: List of parsed directory items
        """
        has_subdirs = False
        for items in parsed_items:
            try:
                if len(items) < 9:
                    continue
                    
                name = items[8]
                perms = items[0]
                is_dir = perms.startswith('d')
                
                # Only process directories, skip . and ..
                if is_dir and name not in ['.', '..']:
                    has_subdirs = True
                    # Construct full path
                    if parent_path == '/':
                        full_path = '/' + name
                    else:
                        full_path = parent_path.rstrip('/') + '/' + name
                    
                    # Add if not already in tree
                    if full_path not in self.remoteTreeItems:
                        child_item = QtWidgets.QTreeWidgetItem(parent_item, [name])
                        child_item.setData(0, QtCore.Qt.ItemDataRole.UserRole, full_path)
                        self.remoteTreeItems[full_path] = child_item
                        # Add dummy child to show expand arrow (will be removed on expansion)
                        dummy = QtWidgets.QTreeWidgetItem(child_item, [""])
                        child_item.setData(0, QtCore.Qt.ItemDataRole.UserRole + 1, True)  # Mark as not yet expanded
            except Exception as e:
                continue
    
    def _expandAndSelectTreePath(self, path):
        """Expand tree to show path and select the item."""
        if not path or path not in self.remoteTreeItems:
            return
        
        # Get all parent paths that need to be expanded
        paths_to_expand = []
        if path == '/':
            # Root path, just select it
            paths_to_expand = ['/']
        else:
            parts = [p for p in path.split('/') if p]
            current_path = '/'
            paths_to_expand.append('/')  # Always include root
            for part in parts:
                current_path = current_path.rstrip('/') + '/' + part
                if current_path in self.remoteTreeItems:
                    paths_to_expand.append(current_path)
        
        # Expand each parent (except the target)
        for p in paths_to_expand[:-1]:
            item = self.remoteTreeItems[p]
            if not item.isExpanded():
                self.remoteTree.expandItem(item)
        
        # Select and make visible the target item
        target_item = self.remoteTreeItems[path]
        self.remoteTree.setCurrentItem(target_item)
        self.remoteTree.scrollToItem(target_item)
    
    def remoteTreeItemExpanded(self, item):
        """When a tree item is expanded, load its children."""
        # Check if this item has already been expanded
        already_expanded = item.data(0, QtCore.Qt.ItemDataRole.UserRole + 1)
        if already_expanded == False:
            return  # Already loaded
        
        # Remove all dummy/empty children
        children_to_remove = []
        for i in range(item.childCount()):
            child = item.child(i)
            if child.text(0) == "":
                children_to_remove.append(child)
        
        for child in children_to_remove:
            item.removeChild(child)
        
        # Mark as expanded
        item.setData(0, QtCore.Qt.ItemDataRole.UserRole + 1, False)
        
        # Get the path for this item
        path = item.data(0, QtCore.Qt.ItemDataRole.UserRole)
        if not path:
            return
        
        # Save current path
        original_path = self.currentRemotePath
        
        # Navigate to this folder to get its contents
        self.ftpLogic.changeWD(path)
        self.ftpLogic.startPassiveDTPconnection()
        self.ftpLogic.getList()
        
        # Get and parse directory list
        dir_list = self.ftpLogic.returnDirList()
        parsed_items, _, _, _ = self._parseDirectoryData(dir_list)
        
        # Add children to tree
        self._addTreeChildren(item, path, parsed_items)
        
        # Return to original path
        if original_path != path:
            self.ftpLogic.changeWD(original_path)
    
    def remoteTreeItemClicked(self, item, column):
        path = item.data(0, QtCore.Qt.ItemDataRole.UserRole)
        if path and path != self.currentRemotePath:
            # Switch to the directory
            self.ftpLogic.changeWD(path)
            self.ftpLogic.startPassiveDTPconnection()
            self.ftpLogic.getList()
            # Only refresh table, not the tree
            self.refreshRemoteTable()

    def remoteTableDoubleClicked(self, row, column):
        name_item = self.remotedir.item(row, 0)
        if not name_item: return
        name = name_item.text()
        
        if name == '..':
            self.openDir('..')
            return
            
        # Check if dir
        perm_item = self.remotedir.item(row, 4)
        is_dir = False
        if perm_item and perm_item.text().startswith('d'):
            is_dir = True
        
        if is_dir:
            self.openDir(name)
        else:
            self.downloadFile(name)

    def openDir(self, folderName):
        """Navigate to a directory (used by double-click on table)."""
        # Change to the directory
        self.ftpLogic.changeWD(folderName)
        self.ftpLogic.startPassiveDTPconnection()
        self.ftpLogic.getList()
        # Only refresh table to avoid losing tree state
        self.refreshRemoteTable()
        # Update tree for the new location
        self._updateRemoteTree()
        # Expand and select the current path in tree
        self._expandAndSelectTreePath(self.currentRemotePath)

    # --- File Operations ---
    def uploadFile(self, filePath):
        # Ensure we are in the correct remote directory
        if self.currentRemotePath != self.ftpLogic.pwd:
             self.ftpLogic.changeWD(self.currentRemotePath)

        # Get file info
        filename = os.path.basename(filePath)
        file_size = os.path.getsize(filePath) if os.path.isfile(filePath) else 0
        
        # Add to queue
        queue_row = self.addToQueue(filename, "上传", file_size)
        
        try:
            # Update status
            self.updateTransferStatus(f"正在上传: {filename}")
            
            # Update queue status
            self.queueTable.setItem(queue_row, 2, QtWidgets.QTableWidgetItem("传输中"))
            
            self.ftpLogic.startPassiveDTPconnection()
            self.ftpLogic.uploadFile(filePath)
            
            # Success - mark as completed in queue instead of removing
            complete_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.queueTable.setItem(queue_row, 2, QtWidgets.QTableWidgetItem("已完成"))
            self.queueTable.setItem(queue_row, 3, QtWidgets.QTableWidgetItem("100%"))
            
            # Also add to success table
            self.moveToSuccess(filename, "上传", file_size, "完成", complete_time)
            
            self.statusMSG()
            self.generateLogTable()
            
            # Refresh remote view after upload
            self.ftpLogic.startPassiveDTPconnection()
            self.ftpLogic.getList()
            self.refreshRemoteView()
            
        except Exception as e:
            # Failed - mark as failed in queue
            error_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.queueTable.setItem(queue_row, 2, QtWidgets.QTableWidgetItem("失败"))
            self.queueTable.setItem(queue_row, 5, QtWidgets.QTableWidgetItem(str(e)[:50]))
            
            # Also add to failed table
            self.moveToFailed(filename, "上传", file_size, str(e), error_time)
        finally:
            self.updateTransferStatus("空闲")
            self.transferProgressBar.setValue(0)

    def downloadFile(self, fileName):
        # Get current local path
        local_path = os.path.join(self.currentLocalPath, fileName)
        
        # Get file size from remote table
        file_size = 0
        for row in range(self.remotedir.rowCount()):
            item = self.remotedir.item(row, 0)
            if item and item.text() == fileName:
                size_item = self.remotedir.item(row, 2)
                if size_item:
                    try:
                        file_size = int(size_item.text().replace(',', ''))
                    except:
                        pass
                break
        
        # Add to queue
        queue_row = self.addToQueue(fileName, "下载", file_size)
        
        try:
            # Update status
            self.updateTransferStatus(f"正在下载: {fileName}")
            
            # Update queue status
            self.queueTable.setItem(queue_row, 2, QtWidgets.QTableWidgetItem("传输中"))

            self.ftpLogic.startPassiveDTPconnection()
            self.ftpLogic.downloadFileTo(fileName, local_path)
            
            # Success - mark as completed
            complete_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.queueTable.setItem(queue_row, 2, QtWidgets.QTableWidgetItem("已完成"))
            self.queueTable.setItem(queue_row, 3, QtWidgets.QTableWidgetItem("100%"))
            
            # Also add to success table
            self.moveToSuccess(fileName, "下载", file_size, "完成", complete_time)
            
            self.statusMSG()
            self.generateLogTable()
            self.refreshLocalView(self.currentLocalPath)
            
        except Exception as e:
            # Failed - mark as failed
            error_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.queueTable.setItem(queue_row, 2, QtWidgets.QTableWidgetItem("失败"))
            self.queueTable.setItem(queue_row, 5, QtWidgets.QTableWidgetItem(str(e)[:50]))
            
            # Also add to failed table
            self.moveToFailed(fileName, "下载", file_size, str(e), error_time)
        finally:
            self.updateTransferStatus("空闲")
            self.transferProgressBar.setValue(0)
    
    def downloadFileToPath(self, fileName, local_path):
        """Download a file to a specific local path."""
        # Get file size from remote table
        file_size = 0
        for row in range(self.remotedir.rowCount()):
            item = self.remotedir.item(row, 0)
            if item and item.text() == fileName:
                size_item = self.remotedir.item(row, 2)
                if size_item:
                    try:
                        file_size = int(size_item.text().replace(',', ''))
                    except:
                        pass
                break
        
        # Add to queue
        queue_row = self.addToQueue(fileName, "下载", file_size)
        
        try:
            # Update status
            self.updateTransferStatus(f"正在下载: {fileName}")
            
            # Update queue status
            self.queueTable.setItem(queue_row, 2, QtWidgets.QTableWidgetItem("传输中"))
            
            self.ftpLogic.startPassiveDTPconnection()
            self.ftpLogic.downloadFileTo(fileName, local_path)
            
            # Success - mark as completed
            complete_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.queueTable.setItem(queue_row, 2, QtWidgets.QTableWidgetItem("已完成"))
            self.queueTable.setItem(queue_row, 3, QtWidgets.QTableWidgetItem("100%"))
            
            # Also add to success table
            self.moveToSuccess(fileName, "下载", file_size, "完成", complete_time)
            
            self.statusMSG()
            self.generateLogTable()
            # Refresh the parent directory
            parent_dir = os.path.dirname(local_path)
            self.refreshLocalView(parent_dir)
            
        except Exception as e:
            # Failed - mark as failed
            error_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.queueTable.setItem(queue_row, 2, QtWidgets.QTableWidgetItem("失败"))
            self.queueTable.setItem(queue_row, 5, QtWidgets.QTableWidgetItem(str(e)[:50]))
            
            # Also add to failed table
            self.moveToFailed(fileName, "下载", file_size, str(e), error_time)
        finally:
            self.updateTransferStatus("空闲")
            self.transferProgressBar.setValue(0)

    def _upload_folder_thread(self, local_dir, remote_base):
        folder_name = os.path.basename(local_dir)
        self.updateTransferStatus(f"正在上传文件夹: {folder_name}")
        
        # Collect all files to upload
        files_to_upload = []
        for dirpath, dirnames, filenames in os.walk(local_dir):
            for fname in filenames:
                local_file = os.path.join(dirpath, fname)
                rel_path = os.path.relpath(local_file, local_dir)
                file_size = os.path.getsize(local_file) if os.path.isfile(local_file) else 0
                files_to_upload.append((local_file, rel_path, file_size))
        
        # Add all files to queue on main thread
        queue_rows = {}
        for local_file, rel_path, file_size in files_to_upload:
            row = self.queueTable.rowCount()
            QtCore.QMetaObject.invokeMethod(
                self, "_addToQueueFromThread",
                QtCore.Qt.ConnectionType.BlockingQueuedConnection,
                QtCore.Q_ARG(str, rel_path),
                QtCore.Q_ARG(str, "上传"),
                QtCore.Q_ARG(int, file_size),
                QtCore.Q_ARG(int, row)
            )
            queue_rows[rel_path] = row
        
        try:
            # Upload with file-by-file progress tracking
            self._upload_folder_with_queue(local_dir, remote_base, queue_rows)
            self.updateTransferProgress(100, "上传完成")
        except Exception as e:
            print(e)
            self.updateTransferProgress(0, "上传失败")
        finally:
            self.updateTransferStatus("空闲")
        
        # Refresh UI on main thread
        QtCore.QMetaObject.invokeMethod(self, "refreshRemoteViewWithConn", QtCore.Qt.ConnectionType.QueuedConnection)
    
    @QtCore.pyqtSlot(str, str, int, int)
    def _addToQueueFromThread(self, filename, direction, size, expected_row):
        """Thread-safe method to add file to queue."""
        row = self.queueTable.rowCount()
        self.queueTable.insertRow(row)
        
        self.queueTable.setItem(row, 0, QtWidgets.QTableWidgetItem(filename))
        self.queueTable.setItem(row, 1, QtWidgets.QTableWidgetItem(direction))
        self.queueTable.setItem(row, 2, QtWidgets.QTableWidgetItem("等待中"))
        self.queueTable.setItem(row, 3, QtWidgets.QTableWidgetItem("0%"))
        self.queueTable.setItem(row, 4, QtWidgets.QTableWidgetItem(str(size)))
        self.queueTable.setItem(row, 5, QtWidgets.QTableWidgetItem(""))
    
    @QtCore.pyqtSlot(int, str)
    def _updateQueueStatus(self, row, status):
        """Update queue item status from thread."""
        if row < self.queueTable.rowCount():
            self.queueTable.setItem(row, 2, QtWidgets.QTableWidgetItem(status))
    
    @QtCore.pyqtSlot(int, str)
    def _updateQueueProgress(self, row, progress):
        """Update queue item progress from thread."""
        if row < self.queueTable.rowCount():
            self.queueTable.setItem(row, 3, QtWidgets.QTableWidgetItem(progress))
    
    @QtCore.pyqtSlot(str, str, int, str)
    def _moveToSuccessFromThread(self, filename, direction, size, complete_time):
        """Thread-safe method to move item to success table."""
        row = self.successTable.rowCount()
        self.successTable.insertRow(row)
        self.successTable.setItem(row, 0, QtWidgets.QTableWidgetItem(filename))
        self.successTable.setItem(row, 1, QtWidgets.QTableWidgetItem(direction))
        self.successTable.setItem(row, 2, QtWidgets.QTableWidgetItem(str(size)))
        self.successTable.setItem(row, 3, QtWidgets.QTableWidgetItem(""))  # Speed placeholder
        self.successTable.setItem(row, 4, QtWidgets.QTableWidgetItem(complete_time))
    
    @QtCore.pyqtSlot(str, str, int, str, str)
    def _moveToFailedFromThread(self, filename, direction, size, error_msg, error_time):
        """Thread-safe method to move item to failed table."""
        row = self.failedTable.rowCount()
        self.failedTable.insertRow(row)
        self.failedTable.setItem(row, 0, QtWidgets.QTableWidgetItem(filename))
        self.failedTable.setItem(row, 1, QtWidgets.QTableWidgetItem(direction))
        self.failedTable.setItem(row, 2, QtWidgets.QTableWidgetItem(str(size)))
        self.failedTable.setItem(row, 3, QtWidgets.QTableWidgetItem(error_msg))
        self.failedTable.setItem(row, 4, QtWidgets.QTableWidgetItem(error_time))
    
    def _upload_folder_with_queue(self, local_path, remote_base, queue_rows):
        """Upload folder with per-file queue updates."""
        if not os.path.exists(local_path):
            return

        local_path = os.path.abspath(local_path)
        remote_base = remote_base.rstrip('/') if remote_base != '/' else '/'
        
        # Navigate to base directory
        self.ftpLogic.changeWD('/')
        if remote_base != '/':
            parts = [p for p in remote_base.strip('/').split('/') if p]
            current_path = ''
            for p in parts:
                current_path += '/' + p
                self.ftpLogic.changeWD(current_path)
                if self.ftpLogic.errorResp:
                    parent_path = '/' + '/'.join(current_path.strip('/').split('/')[:-1])
                    if parent_path == '//':
                        parent_path = '/'
                    self.ftpLogic.changeWD(parent_path)
                    self.ftpLogic.makeDir(p)
                    self.ftpLogic.changeWD(current_path)

        # Upload files
        for dirpath, dirnames, filenames in os.walk(local_path):
            rel = os.path.relpath(dirpath, local_path)
            
            if rel != '.':
                if remote_base == '/':
                    remote_dir = '/' + rel.replace(os.sep, '/')
                else:
                    remote_dir = remote_base + '/' + rel.replace(os.sep, '/')
                
                rel_parts = rel.split(os.sep)
                current_remote = remote_base
                
                for part in rel_parts:
                    parent_remote = current_remote
                    if current_remote == '/':
                        current_remote = '/' + part
                    else:
                        current_remote = current_remote.rstrip('/') + '/' + part
                    
                    self.ftpLogic.changeWD(current_remote)
                    if self.ftpLogic.errorResp:
                        self.ftpLogic.changeWD(parent_remote)
                        self.ftpLogic.makeDir(part)
                        self.ftpLogic.changeWD(current_remote)
            else:
                self.ftpLogic.changeWD(remote_base)

            # Upload each file
            for fname in filenames:
                local_file = os.path.join(dirpath, fname)
                rel_file_path = os.path.relpath(local_file, local_path)
                
                if rel_file_path in queue_rows:
                    row = queue_rows[rel_file_path]
                    
                    try:
                        # Update queue status to transferring
                        QtCore.QMetaObject.invokeMethod(
                            self, "_updateQueueStatus",
                            QtCore.Qt.ConnectionType.QueuedConnection,
                            QtCore.Q_ARG(int, row),
                            QtCore.Q_ARG(str, "传输中")
                        )
                        
                        # Upload file with progress tracking
                        file_size = os.path.getsize(local_file)
                        bytes_sent = 0
                        
                        # Start passive DTP connection
                        self.ftpLogic.startPassiveDTPconnection()
                        
                        # Send STOR command and get response
                        self.ftpLogic.send("STOR " + fname)
                        resp = self.ftpLogic.getServerReply()
                        self.ftpLogic.printServerReply(resp)
                        
                        # Check if there's an error
                        if self.ftpLogic.errorResp:
                            raise Exception(f"STOR command failed: {resp}")
                        
                        # Upload file data in chunks
                        with open(local_file, 'rb') as f:
                            while True:
                                chunk = f.read(8192)
                                if not chunk:
                                    break
                                self.ftpLogic.DTPsocket.send(chunk)
                                bytes_sent += len(chunk)
                                
                                # Update progress
                                if file_size > 0:
                                    progress = int((bytes_sent / file_size) * 100)
                                    QtCore.QMetaObject.invokeMethod(
                                        self, "_updateQueueProgress",
                                        QtCore.Qt.ConnectionType.QueuedConnection,
                                        QtCore.Q_ARG(int, row),
                                        QtCore.Q_ARG(str, f"{progress}%")
                                    )
                        
                        # Close DTP connection and get final response
                        self.ftpLogic.DTPsocket.close()
                        resp = self.ftpLogic.getServerReply()
                        self.ftpLogic.printServerReply(resp)
                        
                        # Mark as completed and move to success table
                        QtCore.QMetaObject.invokeMethod(
                            self, "_updateQueueStatus",
                            QtCore.Qt.ConnectionType.QueuedConnection,
                            QtCore.Q_ARG(int, row),
                            QtCore.Q_ARG(str, "已完成")
                        )
                        QtCore.QMetaObject.invokeMethod(
                            self, "_updateQueueProgress",
                            QtCore.Qt.ConnectionType.QueuedConnection,
                            QtCore.Q_ARG(int, row),
                            QtCore.Q_ARG(str, "100%")
                        )
                        
                        # Add to success table
                        complete_time = datetime.datetime.now().strftime("%H:%M:%S")
                        QtCore.QMetaObject.invokeMethod(
                            self, "_moveToSuccessFromThread",
                            QtCore.Qt.ConnectionType.QueuedConnection,
                            QtCore.Q_ARG(str, fname),
                            QtCore.Q_ARG(str, "上传"),
                            QtCore.Q_ARG(int, file_size),
                            QtCore.Q_ARG(str, complete_time)
                        )
                        
                    except Exception as e:
                        print(f"Upload failed for {fname}: {e}")
                        import traceback
                        traceback.print_exc()
                        # Mark as failed and move to failed table
                        QtCore.QMetaObject.invokeMethod(
                            self, "_updateQueueStatus",
                            QtCore.Qt.ConnectionType.QueuedConnection,
                            QtCore.Q_ARG(int, row),
                            QtCore.Q_ARG(str, "失败")
                        )
                        
                        error_time = datetime.datetime.now().strftime("%H:%M:%S")
                        QtCore.QMetaObject.invokeMethod(
                            self, "_moveToFailedFromThread",
                            QtCore.Qt.ConnectionType.QueuedConnection,
                            QtCore.Q_ARG(str, fname),
                            QtCore.Q_ARG(str, "上传"),
                            QtCore.Q_ARG(int, file_size),
                            QtCore.Q_ARG(str, str(e)),
                            QtCore.Q_ARG(str, error_time)
                        )

    def _download_folder_thread(self, remote_dir, local_dir):
        folder_name = os.path.basename(remote_dir)
        self.updateTransferStatus(f"正在下载文件夹: {folder_name}")
        
        # Collect all files first
        files_to_download = []
        try:
            self._collect_remote_files(remote_dir, local_dir, files_to_download)
        except Exception as e:
            print(f"Error collecting files: {e}")
            import traceback
            traceback.print_exc()
        
        # Add all files to queue
        queue_rows = {}
        for remote_file, local_file, file_size in files_to_download:
            rel_path = os.path.relpath(local_file, os.path.dirname(local_dir.rstrip(os.sep)))
            row = self.queueTable.rowCount()
            QtCore.QMetaObject.invokeMethod(
                self, "_addToQueueFromThread",
                QtCore.Qt.ConnectionType.BlockingQueuedConnection,
                QtCore.Q_ARG(str, rel_path),
                QtCore.Q_ARG(str, "下载"),
                QtCore.Q_ARG(int, file_size),
                QtCore.Q_ARG(int, row)
            )
            queue_rows[(remote_file, local_file)] = row
        
        try:
            # Download with file-by-file queue tracking
            self._download_folder_with_queue(remote_dir, local_dir, queue_rows, files_to_download)
            self.updateTransferProgress(100, "下载完成")
        except Exception as e:
            print(f"Download error: {e}")
            import traceback
            traceback.print_exc()
            self.updateTransferProgress(0, "下载失败")
        finally:
            self.updateTransferStatus("空闲")
        
        # Refresh Local View on main thread
        QtCore.QMetaObject.invokeMethod(self, "refreshLocalViewSlot", QtCore.Qt.ConnectionType.QueuedConnection)
    
    def _collect_remote_files(self, remote_dir, local_base, files_list):
        """Recursively collect all files to download."""
        # Save current directory before any operations
        try:
            self.ftpLogic.send('PWD')
            pwd_resp = self.ftpLogic.getServerReply()
            # Extract path from response like '257 "/path" is current directory'
            start = pwd_resp.find('"')
            end = pwd_resp.find('"', start + 1)
            if start != -1 and end != -1:
                original_path = pwd_resp[start+1:end]
            else:
                original_path = '/'
        except:
            original_path = '/'
        
        # Navigate to remote directory
        self.ftpLogic.changeWD(remote_dir)
        if self.ftpLogic.errorResp:
            return
        
        # Get directory listing
        self.ftpLogic.startPassiveDTPconnection()
        self.ftpLogic.getList()
        dir_list = self.ftpLogic.returnDirList()
        parsed_items, _, _, _ = self._parseDirectoryData(dir_list)
        
        # Process each item
        for items in parsed_items:
            if len(items) < 9:
                continue
            
            name = items[8]
            if name in ['.', '..']: 
                continue
            
            perms = items[0]
            is_dir = perms.startswith('d')
            size = items[4]
            
            try:
                file_size = int(size)
            except:
                file_size = 0
            
            if is_dir:
                # Recursively collect from subdirectory
                # Build full remote and local paths
                sub_remote = remote_dir.rstrip('/') + '/' + name if remote_dir != '/' else '/' + name
                sub_local = os.path.join(local_base, name)
                # Ensure local subdirectory exists
                os.makedirs(sub_local, exist_ok=True)
                # Recursively collect files from subdirectory
                self._collect_remote_files(sub_remote, sub_local, files_list)
            else:
                # Add file to list with full paths
                remote_file = remote_dir.rstrip('/') + '/' + name if remote_dir != '/' else '/' + name
                local_file = os.path.join(local_base, name)
                files_list.append((remote_file, local_file, file_size))
        
        # Return to original path
        try:
            self.ftpLogic.changeWD(original_path)
        except Exception as e:
            print(f"Warning: Could not return to original path {original_path}: {e}")
            # Try to at least go to root
            try:
                self.ftpLogic.changeWD('/')
            except:
                pass
    
    def _download_folder_with_queue(self, remote_base, local_path, queue_rows, files_to_download):
        """Download folder with per-file queue updates."""
        # Ensure local directory exists
        os.makedirs(local_path, exist_ok=True)
        
        # Download each file
        for remote_file, local_file, file_size in files_to_download:
            key = (remote_file, local_file)
            if key not in queue_rows:
                continue
            
            row = queue_rows[key]
            
            try:
                # Update status to transferring
                QtCore.QMetaObject.invokeMethod(
                    self, "_updateQueueStatus",
                    QtCore.Qt.ConnectionType.QueuedConnection,
                    QtCore.Q_ARG(int, row),
                    QtCore.Q_ARG(str, "传输中")
                )
                
                # Ensure local directory exists
                local_dir = os.path.dirname(local_file)
                if local_dir:
                    os.makedirs(local_dir, exist_ok=True)
                
                # Parse remote directory and filename - ensure absolute path
                remote_dir = os.path.dirname(remote_file).replace('\\', '/')
                if not remote_dir or remote_dir == '':
                    remote_dir = '/'
                # Ensure absolute path
                if not remote_dir.startswith('/'):
                    remote_dir = '/' + remote_dir
                filename = os.path.basename(remote_file)
                
                # Navigate to root first, then to the file's directory
                self.ftpLogic.changeWD('/')
                if remote_dir != '/':
                    self.ftpLogic.changeWD(remote_dir)
                    if self.ftpLogic.errorResp:
                        raise Exception(f"Failed to change to directory: {remote_dir}")
                
                # Set binary mode
                self.ftpLogic.setMode('I')
                
                # Reset data connection state before starting new connection
                self.ftpLogic.dataConnectionAlive = False
                
                # Start passive connection for this file
                self.ftpLogic.startPassiveDTPconnection()
                if not self.ftpLogic.dataConnectionAlive:
                    raise Exception("Failed to establish data connection")
                
                # Send RETR command
                self.ftpLogic.send("RETR " + filename)
                resp = self.ftpLogic.getServerReply()
                self.ftpLogic.printServerReply(resp)
                
                if self.ftpLogic.errorResp:
                    # Close failed DTP connection and reset state
                    try:
                        self.ftpLogic.DTPsocket.close()
                        self.ftpLogic.dataConnectionAlive = False
                    except:
                        pass
                    raise Exception(f"RETR command failed: {resp}")
                
                # Download file data in chunks
                bytes_received = 0
                with open(local_file, 'wb') as f:
                    while True:
                        try:
                            data = self.ftpLogic.DTPsocket.recv(8192)
                            if not data:
                                break
                            f.write(data)
                            bytes_received += len(data)
                            
                            # Update progress
                            if file_size > 0:
                                progress = int((bytes_received / file_size) * 100)
                                QtCore.QMetaObject.invokeMethod(
                                    self, "_updateQueueProgress",
                                    QtCore.Qt.ConnectionType.QueuedConnection,
                                    QtCore.Q_ARG(int, row),
                                    QtCore.Q_ARG(str, f"{progress}%")
                                )
                        except Exception as recv_error:
                            print(f"Error receiving data: {recv_error}")
                            break
                
                # Close DTP connection and get final response
                try:
                    self.ftpLogic.DTPsocket.close()
                    self.ftpLogic.dataConnectionAlive = False
                    resp = self.ftpLogic.getServerReply()
                    self.ftpLogic.printServerReply(resp)
                except Exception as close_error:
                    print(f"Error closing connection: {close_error}")
                    self.ftpLogic.dataConnectionAlive = False
                
                # Mark as completed and move to success table
                QtCore.QMetaObject.invokeMethod(
                    self, "_updateQueueStatus",
                    QtCore.Qt.ConnectionType.QueuedConnection,
                    QtCore.Q_ARG(int, row),
                    QtCore.Q_ARG(str, "已完成")
                )
                QtCore.QMetaObject.invokeMethod(
                    self, "_updateQueueProgress",
                    QtCore.Qt.ConnectionType.QueuedConnection,
                    QtCore.Q_ARG(int, row),
                    QtCore.Q_ARG(str, "100%")
                )
                
                # Add to success table
                complete_time = datetime.datetime.now().strftime("%H:%M:%S")
                QtCore.QMetaObject.invokeMethod(
                    self, "_moveToSuccessFromThread",
                    QtCore.Qt.ConnectionType.QueuedConnection,
                    QtCore.Q_ARG(str, os.path.basename(local_file)),
                    QtCore.Q_ARG(str, "下载"),
                    QtCore.Q_ARG(int, file_size),
                    QtCore.Q_ARG(str, complete_time)
                )
                
            except Exception as e:
                print(f"Download failed for {remote_file}: {e}")
                import traceback
                traceback.print_exc()
                # Mark as failed and move to failed table
                QtCore.QMetaObject.invokeMethod(
                    self, "_updateQueueStatus",
                    QtCore.Qt.ConnectionType.QueuedConnection,
                    QtCore.Q_ARG(int, row),
                    QtCore.Q_ARG(str, "失败")
                )
                
                error_time = datetime.datetime.now().strftime("%H:%M:%S")
                QtCore.QMetaObject.invokeMethod(
                    self, "_moveToFailedFromThread",
                    QtCore.Qt.ConnectionType.QueuedConnection,
                    QtCore.Q_ARG(str, os.path.basename(local_file)),
                    QtCore.Q_ARG(str, "下载"),
                    QtCore.Q_ARG(int, file_size),
                    QtCore.Q_ARG(str, str(e)),
                    QtCore.Q_ARG(str, error_time)
                )
                
                # Try to close any open DTP connection
                try:
                    if hasattr(self.ftpLogic, 'DTPsocket') and self.ftpLogic.DTPsocket:
                        self.ftpLogic.DTPsocket.close()
                except:
                    pass
        
        # After all files, return to root directory and reset state
        try:
            self.ftpLogic.changeWD('/')
            self.ftpLogic.dataConnectionAlive = False
        except Exception as e:
            print(f"Warning: Could not reset to root directory: {e}")

    @QtCore.pyqtSlot()
    def refreshLocalViewSlot(self):
        self.refreshLocalView(self.currentLocalPath)

    def updateTransferProgress(self, percent, label_text):
        """Update transfer progress in the status panel."""
        QtCore.QMetaObject.invokeMethod(self.transferProgressBar, "setValue", 
                                       QtCore.Qt.ConnectionType.QueuedConnection, 
                                       QtCore.Q_ARG(int, percent))
        QtCore.QMetaObject.invokeMethod(self.currentTransferLabel, "setText", 
                                       QtCore.Qt.ConnectionType.QueuedConnection, 
                                       QtCore.Q_ARG(str, label_text))
    
    def updateConnectionStatus(self, status_text):
        """Update connection status in status panel."""
        self.connectionStatusLabel.setText(f"连接状态: {status_text}")
    
    def updateTransferStatus(self, status_text):
        """Update transfer status in status panel."""
        self.transferStatusLabel.setText(f"传输状态: {status_text}")
    
    def updateQueueTableProgress(self, row, percent, speed_text):
        """Update progress for a specific queue item."""
        if row < self.queueTable.rowCount():
            # Update progress
            progress_item = QtWidgets.QTableWidgetItem(f"{percent}%")
            self.queueTable.setItem(row, 3, progress_item)
            # Update speed
            speed_item = QtWidgets.QTableWidgetItem(speed_text)
            self.queueTable.setItem(row, 5, speed_item)
    
    def addToQueue(self, filename, direction, size, file_type='file'):
        """Add a file to the transfer queue.
        direction: '上传' or '下载'
        """
        row = self.queueTable.rowCount()
        self.queueTable.insertRow(row)
        
        self.queueTable.setItem(row, 0, QtWidgets.QTableWidgetItem(filename))
        self.queueTable.setItem(row, 1, QtWidgets.QTableWidgetItem(direction))
        self.queueTable.setItem(row, 2, QtWidgets.QTableWidgetItem("等待中"))
        self.queueTable.setItem(row, 3, QtWidgets.QTableWidgetItem("0%"))
        self.queueTable.setItem(row, 4, QtWidgets.QTableWidgetItem(str(size)))
        self.queueTable.setItem(row, 5, QtWidgets.QTableWidgetItem(""))
        
        return row
    

    
    def removeFromQueue(self, row):
        """Remove a row from queue table."""
        if row < self.queueTable.rowCount():
            self.queueTable.removeRow(row)

    def statusMSG(self):
        """Update status from FTP logic - kept for compatibility."""
        # Now we use the status panel instead
        pass

    def generateLogTable(self):
        """Update the FTP command log window."""
        comm_list = self.ftpLogic.getComm()
        self.statusWindow.setRowCount(len(comm_list))
        
        # Display in reverse order (newest first)
        for row in range(len(comm_list)):
            message = comm_list[len(comm_list) - row - 1]
            self.statusWindow.setItem(row, 0, QtWidgets.QTableWidgetItem(message))
        
        self.ftpLogic.clearComm()

    # --- Context Menus ---
    def showLocalContextMenu(self, pos):
        index = self.localdir.indexAt(pos)
        menu = QtWidgets.QMenu()
        
        if index.isValid():
            file_path = index.data(QtCore.Qt.ItemDataRole.UserRole)
            
            # Skip if no valid path data
            if not file_path or file_path == "..":
                return

            uploadAction = menu.addAction("上传")
            addToQueueAction = menu.addAction("添加到队列")
            openAction = menu.addAction("打开")
            editAction = menu.addAction("编辑")
            renameAction = menu.addAction("重命名")
            deleteAction = menu.addAction("删除")
            
            action = menu.exec(self.localdir.viewport().mapToGlobal(pos))
            
            if action == uploadAction:
                if os.path.isfile(file_path):
                    self.uploadFile(file_path)
                elif os.path.isdir(file_path):
                    folder_name = os.path.basename(file_path)
                    # Upload to currentRemotePath/folder_name
                    if self.currentRemotePath == '/':
                        remote_base = '/' + folder_name
                    else:
                        remote_base = self.currentRemotePath.rstrip('/') + '/' + folder_name
                    
                    t = threading.Thread(target=self._upload_folder_thread, args=(file_path, remote_base))
                    t.daemon = True
                    t.start()
            elif action == addToQueueAction:
                print(f"Added {file_path} to queue (Not implemented)")
            elif action == openAction:
                QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(file_path))
            elif action == editAction:
                # Simple edit: open with system default
                QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(file_path))
            elif action == renameAction:
                old_name = os.path.basename(file_path)
                new_name, ok = QtWidgets.QInputDialog.getText(None, "重命名", "请输入新名称:", text=old_name)
                if ok and new_name:
                    new_path = os.path.join(os.path.dirname(file_path), new_name)
                    os.rename(file_path, new_path)
                    self.refreshLocalView(self.currentLocalPath)
            elif action == deleteAction:
                confirm = QtWidgets.QMessageBox.question(None, "确认删除", f"确定要删除 {os.path.basename(file_path)} 吗?", 
                                                       QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
                if confirm == QtWidgets.QMessageBox.StandardButton.Yes:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    else:
                        import shutil
                        shutil.rmtree(file_path)
                    self.refreshLocalView(self.currentLocalPath)
        else:
            # Empty space on local
            refreshAction = menu.addAction("刷新")
            action = menu.exec(self.localdir.viewport().mapToGlobal(pos))
            if action == refreshAction:
                self.refreshLocalView(self.currentLocalPath)

    def showRemoteContextMenu(self, pos):
        menu = QtWidgets.QMenu()
        item = self.remotedir.itemAt(pos)
        
        selected_name = None
        is_dir = False
        downloadAction = None
        addToQueueAction = None
        openAction = None
        editAction = None
        renameAction = None
        deleteAction = None
        
        if item:
            row = item.row()
            name_item = self.remotedir.item(row, 0)
            if name_item:
                selected_name = name_item.text()
                if selected_name != '..':
                    perm_item = self.remotedir.item(row, 4)
                    if perm_item and perm_item.text().startswith('d'):
                        is_dir = True
                    
                    downloadAction = menu.addAction("下载")
                    addToQueueAction = menu.addAction("添加到队列")
                    menu.addSeparator()
                    openAction = menu.addAction("打开")
                    editAction = menu.addAction("编辑")
                    menu.addSeparator()
                    renameAction = menu.addAction("重命名")
                    deleteAction = menu.addAction("删除")
                    menu.addSeparator()

        newFolderAction = menu.addAction("新建文件夹")
        refreshAction = menu.addAction("刷新")
        
        action = menu.exec(self.remotedir.viewport().mapToGlobal(pos))
        
        if action == newFolderAction:
            dirName, ok = QtWidgets.QInputDialog.getText(None, "新建文件夹", "请输入文件夹名称:")
            if ok and dirName:
                self.ftpLogic.makeDir(dirName)
                self.statusMSG()
                self.generateLogTable()
                self.refreshRemoteViewWithConn()
                
        elif action == refreshAction:
            self.refreshRemoteViewWithConn()

        elif selected_name and selected_name != '..':
            if action == downloadAction:
                if is_dir:
                    # Get current local path
                    target_local_path = os.path.join(self.currentLocalPath, selected_name)
                    
                    # Construct full remote path
                    if self.currentRemotePath == '/':
                        full_remote_path = selected_name
                    else:
                        full_remote_path = self.currentRemotePath + '/' + selected_name
                    
                    t = threading.Thread(target=self._download_folder_thread, args=(full_remote_path, target_local_path))
                    t.daemon = True
                    t.start()
                else:
                    self.downloadFile(selected_name)
            
            elif action == addToQueueAction:
                 print(f"Added remote {selected_name} to queue (Not implemented)")

            elif action == openAction:
                 print("Open remote file (Not implemented)")
            
            elif action == editAction:
                 print("Edit remote file (Not implemented)")

            elif action == renameAction:
                new_name, ok = QtWidgets.QInputDialog.getText(None, "重命名", "请输入新名称:", text=selected_name)
                if ok and new_name:
                    self.ftpLogic.rename(selected_name, new_name)
                    self.statusMSG()
                    self.generateLogTable()
                    self.refreshRemoteViewWithConn()

            elif action == deleteAction:
                confirm = QtWidgets.QMessageBox.question(None, "确认删除", f"确定要删除 {selected_name} 吗?", 
                                                       QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
                if confirm == QtWidgets.QMessageBox.StandardButton.Yes:
                    if is_dir:
                        self.ftpLogic.remDir(selected_name)
                    else:
                        self.ftpLogic.deleteFile(selected_name)
                    self.statusMSG()
                    self.generateLogTable()
                    self.refreshRemoteViewWithConn()

    @QtCore.pyqtSlot()
    def refreshRemoteViewWithConn(self):
        """Helper to refresh view after operations, preserving tree state."""
        # Ensure we're in the current directory
        if self.currentRemotePath != self.ftpLogic.pwd:
            self.ftpLogic.changeWD(self.currentRemotePath)
        
        self.ftpLogic.startPassiveDTPconnection()
        self.ftpLogic.getList()
        # Only refresh table and update current tree node, don't rebuild entire tree
        self.refreshRemoteTable()
        self._updateRemoteTree()

    # --- Drag and Drop ---
    def localStartDrag(self, supportedActions):
        """Custom drag start for local tree to include file info."""
        selected_indexes = self.localdir.selectedIndexes()
        if not selected_indexes:
            return
        
        # Get the first selected item (column 0)
        index = selected_indexes[0]
        item = self.localdir.model().itemFromIndex(index)
        if not item:
            return
        
        file_path = item.data(QtCore.Qt.ItemDataRole.UserRole)
        if not file_path or file_path == "..":
            return
        
        # Create mime data with custom format
        mime_data = QtCore.QMimeData()
        mime_data.setData("application/x-ftp-local-file", file_path.encode('utf-8'))
        # Also add as URL for compatibility
        mime_data.setUrls([QtCore.QUrl.fromLocalFile(file_path)])
        
        # Create drag
        drag = QtGui.QDrag(self.localdir)
        drag.setMimeData(mime_data)
        drag.exec(QtCore.Qt.DropAction.CopyAction)
    
    def remoteDragEnterEvent(self, event):
        if event.mimeData().hasUrls() or event.mimeData().hasFormat("application/x-ftp-local-file"):
            event.accept()
        else:
            event.ignore()
    
    def remoteDragMoveEvent(self, event):
        """Accept drag move."""
        if event.mimeData().hasUrls() or event.mimeData().hasFormat("application/x-ftp-local-file"):
            event.accept()
        else:
            event.ignore()

    def remoteDropEvent(self, event):
        # Check if it's from local tree
        if event.mimeData().hasFormat("application/x-ftp-local-file"):
            event.setDropAction(QtCore.Qt.DropAction.CopyAction)
            event.accept()
            
            local_path = event.mimeData().data("application/x-ftp-local-file").data().decode('utf-8')
            
            if os.path.isfile(local_path):
                self.uploadFile(local_path)
            elif os.path.isdir(local_path):
                # Get folder name and create remote path
                folder_name = os.path.basename(local_path)
                if self.currentRemotePath == '/':
                    remote_base = '/' + folder_name
                else:
                    remote_base = self.currentRemotePath.rstrip('/') + '/' + folder_name
                
                t = threading.Thread(target=self._upload_folder_thread, args=(local_path, remote_base))
                t.daemon = True
                t.start()
        
        elif event.mimeData().hasUrls():
            # From external file system
            event.setDropAction(QtCore.Qt.DropAction.CopyAction)
            event.accept()
            for url in event.mimeData().urls():
                local_path = url.toLocalFile()
                if os.path.isfile(local_path):
                    self.uploadFile(local_path)
                elif os.path.isdir(local_path):
                    # Get folder name and create remote path
                    folder_name = os.path.basename(local_path)
                    if self.currentRemotePath == '/':
                        remote_base = '/' + folder_name
                    else:
                        remote_base = self.currentRemotePath.rstrip('/') + '/' + folder_name
                    
                    t = threading.Thread(target=self._upload_folder_thread, args=(local_path, remote_base))
                    t.daemon = True
                    t.start()
    
    def remoteStartDrag(self, supportedActions):
        """Custom drag start for remote table to include file info."""
        selected_items = self.remotedir.selectedItems()
        if not selected_items:
            return
        
        # Get the row of the first selected item
        row = self.remotedir.row(selected_items[0])
        name_item = self.remotedir.item(row, 0)
        if not name_item or name_item.text() == '..':
            return
        
        filename = name_item.text()
        
        # Create mime data with custom format
        mime_data = QtCore.QMimeData()
        mime_data.setText(filename)
        mime_data.setData("application/x-ftp-remote-file", filename.encode('utf-8'))
        
        # Create drag
        drag = QtGui.QDrag(self.remotedir)
        drag.setMimeData(mime_data)
        drag.exec(QtCore.Qt.DropAction.CopyAction)
    
    def localDragEnterEvent(self, event):
        """Accept drag from remote table or external files."""
        if event.mimeData().hasFormat("application/x-ftp-remote-file") or event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
    
    def localDragMoveEvent(self, event):
        """Accept drag move."""
        if event.mimeData().hasFormat("application/x-ftp-remote-file") or event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
    
    def localDropEvent(self, event):
        """Handle drop on local directory - download from remote or copy from external."""
        # Check if it's from remote table
        if event.mimeData().hasFormat("application/x-ftp-remote-file"):
            event.setDropAction(QtCore.Qt.DropAction.CopyAction)
            event.accept()
            
            filename = event.mimeData().data("application/x-ftp-remote-file").data().decode('utf-8')
            
            # Get local drop target directory
            pos = event.position().toPoint() if hasattr(event.position(), 'toPoint') else event.pos()
            index = self.localdir.indexAt(pos)
            if index.isValid():
                # Get the path from the model
                file_model = self.localdir.model()
                item = file_model.itemFromIndex(index)
                if item:
                    item_path = item.data(QtCore.Qt.ItemDataRole.UserRole)
                    if item_path and os.path.isdir(item_path):
                        local_dir = item_path
                    else:
                        local_dir = self.currentLocalPath
                else:
                    local_dir = self.currentLocalPath
            else:
                # Use current local directory
                local_dir = self.currentLocalPath
            
            # Download to target directory
            local_path = os.path.join(local_dir, filename)
            
            # Check if it's a directory or file
            for row in range(self.remotedir.rowCount()):
                item = self.remotedir.item(row, 0)
                if item and item.text() == filename:
                    perm_item = self.remotedir.item(row, 4)
                    if perm_item and perm_item.text().startswith('d'):
                        # It's a directory - use absolute remote path
                        # Get current remote directory
                        current_remote = self.ftpLogic.pwd if hasattr(self.ftpLogic, 'pwd') else '/'
                        if current_remote == '/':
                            full_remote_path = '/' + filename
                        else:
                            full_remote_path = current_remote.rstrip('/') + '/' + filename
                        
                        t = threading.Thread(target=self._download_folder_thread, args=(full_remote_path, local_path))
                        t.daemon = True
                        t.start()
                    else:
                        # It's a file
                        self.downloadFileToPath(filename, local_path)
                    break
        
        elif event.mimeData().hasUrls():
            # Handle drop from external file system (copy to local)
            event.setDropAction(QtCore.Qt.DropAction.CopyAction)
            event.accept()
            # Let the default handler manage this
            QtWidgets.QTreeView.dropEvent(self.localdir, event)

def Main():
    clientName = socket.gethostbyname(socket.gethostname())
    app = QtWidgets.QApplication(sys.argv)
    
    # Set application icon
    icon_path = os.path.join(os.path.dirname(__file__), 'icon.png')
    if os.path.exists(icon_path):
        app.setWindowIcon(QtGui.QIcon(icon_path))
    
    MainWindow = QtWidgets.QMainWindow()
    
    # Set window icon
    if os.path.exists(icon_path):
        MainWindow.setWindowIcon(QtGui.QIcon(icon_path))
    
    client = FTPclient(clientName)
    application = cleintInterface(MainWindow, client)
    MainWindow.show()
    sys.exit(app.exec())

Main()
