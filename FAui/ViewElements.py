from PyQt6 import QtWidgets


class ViewElements:
    # -> LCD
    lcdResultCount: QtWidgets.QLCDNumber = None
    # -> WebSocket
    editChatHost = None
    btnChatConnect = None
    editChatInput = None
    listChatMessages = None
    toggleChatIsConnected = None
    chatserver = None
    btnChatServerStart = None
    toggleChatServerIsRunning = None
    listChatProcessResponse: QtWidgets.QListWidget = None
    # -> Download
    btnDownloadUrl = None
    btnCrawlerUrl: QtWidgets.QPushButton = None

    # -> Statistics
    lblArticleCount = None
    lblArticleCountNumber: QtWidgets.QLabel = None
    lblResultCount = None
    lblResultCountNumber: QtWidgets.QLabel = None
    # -> Search
    btnSearch: QtWidgets.QPushButton = None
    editSearchText: QtWidgets.QLineEdit = None
    editSearchLimit: QtWidgets.QTextEdit = None
    editSearchPage: QtWidgets.QTextEdit = None

    toggleOnDate: QtWidgets.QCheckBox = None
    toggleBeforeDate: QtWidgets.QCheckBox = None
    toggleAfterDate: QtWidgets.QCheckBox = None
    dateSearchSpecific: QtWidgets.QDateEdit = None

    toggleRangeEnable: QtWidgets.QCheckBox = None
    dateRangeSearchBefore: QtWidgets.QDateEdit = None
    dateRangeSearchAfter: QtWidgets.QDateEdit = None

    toggleSummary: QtWidgets.QCheckBox = False
    listArticlesByTitle: QtWidgets.QListWidget = None
    # -> Article Details
    editDetailsDatePublished: QtWidgets.QLineEdit = None
    editDetailsAuthor: QtWidgets.QLineEdit = None
    editDetailsCategory: QtWidgets.QLineEdit = None
    editDetailsScore: QtWidgets.QLineEdit = None
    editDetailsSource: QtWidgets.QLineEdit = None
    editDetailsUrl: QtWidgets.QLineEdit = None
    txtBody: QtWidgets.QTextEdit = None
    lblTitle: QtWidgets.QLabel = None
    # -> Server Details
    editServerName = None
    editServerHost = None
    editServerPort = None
    editServerUser = None
    editServerPassword = None
    btnServerConnect: QtWidgets.QPushButton = None
    btnServerDisconnect: QtWidgets.QPushButton = None
    toggleServerIsConnected: QtWidgets.QCheckBox = False
    # -> Tabs
    tabWidget = None
    # cache
    jpro = None
    current_articles = {}
    current_article = {}