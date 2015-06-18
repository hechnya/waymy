function addFavorite(a) {
    var title = document.title;
    var url = document.location;
    try {
        // Internet Explorer
        window.external.AddFavorite(url, title);
    }
    catch (e) {
        try {
            // Mozilla
            window.sidebar.addPanel(title, url, "");
        }
        catch (e) {
            // Opera
            if (typeof(opera)=="object" || window.sidebar) {
                a.rel="sidebar";
                a.title=title;
                a.url=url;
                a.href=url;
                return true;
            }
            else {
                // Unknown
                alert('Нажмите Ctrl-D чтобы добавить страницу в закладки');
            }
        }
    }
    return false;
}