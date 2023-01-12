#/usr/bin/env python3

# from PyQt6 import QtWidgets
import FQt
from F.CLASS import FAIR_CALLBACK_CHANNEL
from FAui.MongoQ import harkPro
from F import LIST, DICT, DATE, OS
from FQt.MainWindow import FairMainWindow
from FCM import MCServers
from FAui.ViewElements import ViewElements

ui_file_path = f"{OS.get_cwd()}/mainw.ui"

"""
 -> Everything/Widget should be named exactly the name
    : QtDesigner -> btnSearch
    : Class Variable -> btnSearch
    : Action Function -> action_btnSearch
"""

class LucasUI(FairMainWindow, ViewElements):
    """ Variables are in ViewElements """
    searchMode = "default"
    fairclient = None
    allArticles = []

    def __init__(self):
        super(LucasUI, self).__init__()
        # -> Load UI Template File
        self.bind_ui(ui_file_path)
        # -> Do Custom Work
        # # -> Finish Up
        self.show()
        self.toggleChatServerIsRunning.setEnabled(False)
        self.toggleServerIsConnected.setEnabled(False)
        self.btnDownloadUrl.setEnabled(False)
        self.btnCrawlerUrl.setEnabled(False)
        self.toggleChatProcessIsRunning.setEnabled(False)
        self.toggleRangeEnable.setEnabled(False)

    """ Actions """

    def onClick_btnNext(self, item):
        if not self.current_articles:
            return
        title = self.get_dict("title", self.current_article)
        item = DICT.get_random(self.current_articles)
        newTitle = self.get_dict("title", item)
        if title == newTitle:
            item = DICT.get_random(self.current_articles)
        self.set_current_article(item)

    def onToggled_checkSummary(self, item):
        self.toggleSummary = item

    def onDoubleClick_listArticlesByTitle(self, item):
        title = item.text()
        new_article = DICT.get(title, self.current_articles)
        self.set_current_article(new_article)
        self.tabWidget.setCurrentIndex(1)

    def onDoubleClick_listEnhancedTickers(self, item):
        ticker = item.text()
        results = self.jpro.jworld.find_world_by_ticker(ticker)
        if results:
            details = ""
            for keyItem in results:
                details += f"\n-> {keyItem}:\n{results[keyItem]}\n"
            self.editEnhancedCompany.setText(str(details))
        else:
            results = self.jpro.jcompany.find_company_by_ticker(ticker)
            if results:
                details = ""
                for keyItem in results:
                    details += f"\n-> {keyItem}:\n{results[keyItem]}\n"
                self.editEnhancedCompany.setText(str(details))

    def onTextChanged_editSearchText(self, item):
        print("onTextChanged", item)

    def onClick_btnSearch(self):
        """ Master Search """
        self._build_search()

    @FAIR_CALLBACK_CHANNEL.subscribe
    def onFairChannelCallback(self, msg):
        print(msg)
        results = self.get_arg("results", msg)
        print(results)
        self._load_new_articles(results)
        pass

    def _load_new_articles(self, results):
        self.set_current_articles(results)
        self.allArticles.append(results)
        firstArt = LIST.get(0, results)
        self.set_current_article(firstArt)

    def _build_search(self):
        searchTerm = self.editSearchText.text()
        todaysDate = DATE.get_now_month_day_year_str()
        earliestDate = DATE.TO_DATETIME("January 01 1900")
        # -> Limit & Page
        limit = self.editSearchLimit.toPlainText()
        if limit in ["", " "]:
            limit = 10
        page = self.editSearchPage.toPlainText()
        if page in ["", " "]:
            page = 1
        limit = int(limit)
        page = int(page)
        rawSpecificDate = self.dateSearchSpecific.text()
        if self.searchMode == "dateRange":
            print("search -> dateRange")
            rawDateRangeBefore = self.dateRangeSearchBefore.text()
            rawDateRangeAfter = self.dateRangeSearchAfter.text()
            results = self.jpro.search_by_date_range(searchTerm=searchTerm, gte=rawDateRangeAfter, lte=rawDateRangeBefore, limit=limit)
        elif self.searchMode == "onDate":
            print("search -> onDate")
            results = self.jpro.search_by_date_range(searchTerm=searchTerm, gte=rawSpecificDate, lte=rawSpecificDate, limit=limit)
        elif self.searchMode == "beforeDate":
            print("search -> beforeDate")
            results = self.jpro.search_by_date_range(searchTerm=searchTerm, gte=earliestDate, lte=rawSpecificDate, limit=limit)
        elif self.searchMode == "afterDate":
            print("search -> afterDate")
            results = self.jpro.search_by_date_range(searchTerm=searchTerm, gte=rawSpecificDate, lte=todaysDate, limit=limit)
        else:
            print("search -> General Search All")
            results = self.jpro.search_all(search_term=searchTerm, limit=limit, page=page)
        self._load_new_articles(results)


    """ Article Search """

    def onToggled_toggleRangeEnable(self, item):
        self._reset_toggleDates()
        self.toggleRangeEnable.setChecked(item)
        self.searchMode = "dateRange"

    def onToggled_toggleOnDate(self, item):
        if item:
            self.__toggleOnDate(True, True)
            self.searchMode = "onDate"
            self.__toggleBeforeDate(False, False)
            self.__toggleAfterDate(False, False)
        else:
            self._reset_toggleDates()

    def onToggled_toggleBeforeDate(self, item):
        if item:
            self.__toggleOnDate(False, False)
            self.__toggleBeforeDate(True, True)
            self.searchMode = "beforeDate"
            self.__toggleAfterDate(False, False)
        else:
            self._reset_toggleDates()

    def onToggled_toggleAfterDate(self, item):
        if item:
            self.__toggleOnDate(False, False)
            self.__toggleBeforeDate(False, False)
            self.__toggleAfterDate(True, True)
            self.searchMode = "afterDate"
        else:
            self._reset_toggleDates()

    def _reset_toggleDates(self):
        self.__toggleOnDate(False, True)
        self.__toggleBeforeDate(False, True)
        self.__toggleAfterDate(False, True)

    def __toggleOnDate(self, setTrue, isEnabled=True):
        self.toggleOnDate.setEnabled(isEnabled)
        self.toggleOnDate.setChecked(setTrue)

    def __toggleBeforeDate(self, setTrue, isEnabled=True):
        self.toggleBeforeDate.setEnabled(isEnabled)
        self.toggleBeforeDate.setChecked(setTrue)

    def __toggleAfterDate(self, setTrue, isEnabled=True):
        self.toggleAfterDate.setEnabled(isEnabled)
        self.toggleAfterDate.setChecked(setTrue)

    # -> Reports...

    def onClick_btnMetaLand(self):
        self.onClick_btnClear()
        daysBack = int(self.editMetaDaysBack.toPlainText())
        if daysBack <= 0:
            daysBack = 30
        meta_articles = self.jpro.get_meta_feed_v4(daysBack=int(daysBack))
        self.set_current_articles(meta_articles)

    def onClick_btnMetaReport(self):
        self.onClick_btnClear()
        daysBack = int(self.editMetaDaysBack.toPlainText())
        if daysBack <= 0:
            daysBack = 30
        meta_articles = self.jpro.get_meta_feed_v1(daysBack=int(daysBack))
        self.set_current_articles(meta_articles)

    def onClick_btnMetaReport2(self):
        self.onClick_btnClear()
        daysBack = int(self.editMetaDaysBack.toPlainText())
        if daysBack <= 0:
            daysBack = 30
        meta_articles = self.jpro.get_meta_feed_v2(daysBack=int(daysBack))
        self.set_current_articles(meta_articles)

    def onClick_btnMetaCategory(self):
        self.onClick_btnClear()
        meta_articles = self.jpro.get_metaverse_articles()
        self.set_current_articles(meta_articles)

    """ Mongo Server Connect for Articles """
    def onClick_btnServerConnect(self):
        name = self.editServerName.text()
        host = self.editServerHost.text()
        port = self.editServerPort.text()
        dbUri = MCServers.BASE_MONGO_URI(host, port)
        self.jpro = harkPro(dbUri=dbUri, dbName=name)
        if self.jpro and self.jpro.is_connected():
            self.toggleServerIsConnected.setChecked(True)
            self.btnServerConnect.setEnabled(False)
            self.get_server_details()

    def onClick_btnServerDisconnect(self):
        if self.jpro:
            self.jpro.core_client.close()
            self.toggleServerIsConnected.setChecked(False)
            self.btnServerConnect.setEnabled(True)
            self.btnServerDisconnect.setEnabled(False)

    def onClick_btnClear(self):
        self.listArticlesByTitle.clear()
        self.lblResultCountNumber.setText("0")
        self.lblTitle.setText("...")
        self.txtBody.setText("")
        self.clearSearchText()

    def onClick_btnAddFavorite(self):
        title = DICT.get("title", self.current_article)
        self.listFavoriteArticles.addItem(title)

    def onDoubleClick_listFavoriteArticles(self, item):
        title = item.text()
        for art in self.allArticles:
            artTitle = DICT.get("title", art)
            if artTitle == title:
                self.set_current_article(art)
                self.tabWidget.setCurrentIndex(1)

    """Server Details"""
    def get_server_details(self):
        self.set_article_count()

    """ Article Work """
    def set_article_count(self):
        if self.jpro:
            art_count = self.jpro.get_article_count()
            self.lblArticleCountNumber.setText(str(art_count))

    def set_current_articles(self, articles):
        """ Setup Master List of Article Headlines """
        if not articles:
            return
        self.allArticles.append(articles)
        self.allArticles = LIST.flatten(self.allArticles)
        self.listArticlesByTitle.clear()
        count = len(articles)
        self.lcdResultCount.display(int(count))
        self.lblResultCountNumber.setText(str(count))
        isFirst = True
        number = 1
        for art in articles:
            if isFirst:
                self.set_current_article(art)
                isFirst = False
            title = DICT.get("title", art)
            score = DICT.get("score", art, "NoScore")
            date = DICT.get("published_date", art, "NoDate")
            key = f"{number}. [ {score} ] {date} \n{title}\n"
            self.current_articles[key] = art
            self.listArticlesByTitle.addItem(key)
            number += 1

    def set_current_article(self, article):
        """ Setup Single Article to be Read """
        if not article:
            self.txtBody.setText("No Articles Found...")
            return
        isEnhanced = True
        # -> Set Global Current
        self.current_article = article
        # -> Set Title
        title = DICT.get("title", article, default="No Title...")
        self.lblTitle.setText(title)
        #
        pDate = DICT.get("published_date", article)
        self.editDetailsDatePublished.setText(pDate)
        self.editDetailsDatePublished.setEnabled(False)
        author = DICT.get("author", article)
        self.editDetailsAuthor.setText(str(author))
        self.editDetailsAuthor.setEnabled(False)
        source = DICT.get("source", article)
        self.editDetailsSource.setText(source)
        self.editDetailsSource.setEnabled(False)
        url = DICT.get("url", article)
        self.editDetailsUrl.setText(url)
        self.editDetailsUrl.setEnabled(False)
        # -> Set Main Body
        body = DICT.get("body", article, default="No Body...")
        if self.toggleSummary and isEnhanced:
            summary = DICT.get("summary", article, default=False)
            self.txtBody.setText(summary if summary else body)
        else:
            self.txtBody.setText(body)
        self.setup_enhancements(article)

    def setup_basics(self, article):
        pass

    def setup_enhancements(self, article):
        try:
            category = DICT.get("category", article)
            self.editDetailsCategory.setText(category)
            self.editDetailsCategory.setEnabled(False)
            score = DICT.get("score", article)
            self.editDetailsScore.setText(str(score))
            self.editDetailsScore.setEnabled(False)

            self.editEnhancedCompany.setText("")
            # Keywords
            self.listEnhancedKeywords.clear()
            keywords = DICT.get("keywords", article, [])
            tags = DICT.get("tags", article, [])
            all_words = keywords + tags
            all_words = LIST.flatten(all_words)
            if all_words:
                for word in all_words:
                    self.listEnhancedKeywords.addItem(word)
            else:
                self.listEnhancedKeywords.addItem("No Keywords")

            # Tickers
            self.listEnhancedTickers.clear()
            tickers = DICT.get("tickers", article, [])
            # list or dict
            if type(tickers) in [list]:
                for item in tickers:
                    for key in item:
                        self.listEnhancedTickers.addItem(key)
            else:
                for key in tickers:
                    self.listEnhancedTickers.addItem(key)

        except:
            isEnhanced = False
            print("Not Enhanced")

    def clearSearchText(self):
        self.editSearchText.setText("")

if __name__ == '__main__':
    FQt.launchUI(LucasUI)
