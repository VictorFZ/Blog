angularApp.factory('articleFactory', function ($http) {
    function getArticles(success) {
        $http.get("/Articles").success(success);
    }

    return {
        getArticles: getArticles
    };
});