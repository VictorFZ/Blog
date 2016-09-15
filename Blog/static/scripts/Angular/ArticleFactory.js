angularApp.factory('articleFactory', function ($http) {
    function getArticles(success, error) {
        $http.get("/Articles").success(success).error(error);
    }

    function getArticle(id, success, error) {
        $http.get("/Articles/" + id).success(success).error(error);
    }

    function getLoggedUser(success, error) {
        $http.get("/Users/Login").success(success).error(error);
    }

    function loginUser(model, success, error) {
        $http.post("/Users/Login", model).success(success).error(error);
    }

    function logoutUser(success, error) {
        $http.get("/Users/Logout", { teste: "sdf" }).success(success).error(error);
    }

    function signinUser(model, success, error) {
        $http.post("/Users/Sigin", model).success(success).error(error);
    }

    function deleteArticle(oid, success, error) {
        $http.delete("/Articles/" + oid).success(success).error(error);
    }

    function createArticle(article, success, error) {
        $http.post("/Articles", article).success(success).error(error);
    }

    function createComment(articleID, comment, success, error) {
        $http.post("/Articles/"+articleID+"/Comment", comment).success(success).error(error);
    }


    return {
        getArticles: getArticles,
        getArticle: getArticle,
        getLoggedUser: getLoggedUser,
        loginUser: loginUser,
        signinUser: signinUser,
        logoutUser: logoutUser,
        deleteArticle: deleteArticle,
        createArticle: createArticle,
        createComment: createComment
    };
});