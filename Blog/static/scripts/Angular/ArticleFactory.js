angularApp.factory('articleFactory', function ($http) {
    function getArticles(tags, categories, success, error) {
        $http.get("/Articles?tags="+tags+"&categories="+categories).success(success).error(error);
    }

    function getArticle(id, success, error) {
        $http.get("/Articles/" + id).success(success).error(error);
    }

    function getArticleBySlug(slug, success, error) {
        $http.get("/Articles/BySlug/" + slug).success(success).error(error);
    }

    function getCategories(success, error) {
        $http.get("/Categories").success(success).error(error);
    }

    function createCategory(category, success, error) {
        $http.post("/Categories", category).success(success).error(error);
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

    function deleteCategory(oid, success, error) {
        $http.delete("/Categories/" + oid).success(success).error(error);
    }

    function createArticle(article, success, error) {
        $http.post("/Articles", article).success(success).error(error);
    }

	function updateArticle(oid, article, success, error) {
        $http.post("/Articles/" + oid, article).success(success).error(error);
    }

    function createComment(articleID, comment, success, error) {
        $http.post("/Articles/"+articleID+"/Comment", comment).success(success).error(error);
    }


    return {
        getArticles: getArticles,
        getArticleBySlug: getArticleBySlug,
        getArticle: getArticle,
        getLoggedUser: getLoggedUser,
        loginUser: loginUser,
        signinUser: signinUser,
        logoutUser: logoutUser,
        deleteArticle: deleteArticle,
        createArticle: createArticle,
        createComment: createComment,
		    updateArticle: updateArticle,
        createCategory: createCategory,
        getCategories: getCategories,
        deleteCategory: deleteCategory
    };
});
