from CrawlerGUI import CrawlerGUI
from CrawlerActions import CrawlerActions

if __name__ == "__main__":
    actions = CrawlerActions(None)  # 临时为None
    app = CrawlerGUI(actions)
    actions.app = app
    app.mainloop()
