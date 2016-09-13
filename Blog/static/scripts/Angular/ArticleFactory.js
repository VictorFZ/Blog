angularApp.factory('articleFactory', function ($http) {
    function getArticles(success, error) {
        $http.get("/Articles").success(success).error(error);
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

    return {
        getArticles: getArticles,
        getLoggedUser: getLoggedUser,
        loginUser: loginUser,
        signinUser: signinUser,
        logoutUser: logoutUser
    };
});