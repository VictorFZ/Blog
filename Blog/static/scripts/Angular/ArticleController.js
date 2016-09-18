var angularApp = angular.module('MongoApp', ['ngSanitize']);

angularApp.controller('ArticleController', function ($scope, articleFactory) {
    var self = this;

    self.filterTags = "";
    self.filterCategories = "";
    self.hasFilterTags = false;
    self.hasFilterCategories = false;
    self.articleSlug = null;
    self.articleNotFound = false;
	  self.isEditingArticle = false;
	  self.editingArticleID = "";
    self.globalMessageClass = "";
    self.globalMessageShow = false;
    self.globalMessage = "";
    self.globalMessageTitle = "";

    self.loggedUser = null;
    self.loginEmailInput = "";
    self.loginPasswordInput = "";
    self.loginError = false;

    self.signinError = false;
    self.signinMessage = "";

    self.signinEmailInput = "";
    self.signinPasswordInput = "";
    self.signinConfirmPasswordInput = "";
    self.signinNameInput = "";

    self.articles = [];
    self.categories = [];
    self.selectedArticleOid = "";

    self.createCategoryNameInput = "";

    self.createArticleNameInput = "";
    self.createArticleTextInput = "";
    self.createArticleTagsInput = "";
    self.createArticleSlugInput = "";

    self.createArticleCategoriesInput = "";
    self.createArticleError = false;
    self.createArticleMessage = "";

    self.createCategoryError = false;
    self.createCategoryMessage = "";

    function bindTooltips() {
        $(".tooltip-item").tooltip('destroy');
        $(".tooltip-item").tooltip();
    }

    function showModal(id) {
        $("#" + id).modal({
            backdrop: 'static',
            keyboard: false
        }).modal("show");
    }

    function hideModal(id) {
        $("#" + id).modal("hide");
    }

    function loadCategories(){
      articleFactory.getCategories(function (response) {
          self.categories = response;
          if(self.categories != null && self.categories.length > 0){
            $("#create-article-categories-input")[0].selectedIndex = 0;
          }
      }, function () { });
    }

    function loadArticles() {
      self.articleNotFound = false;
      if(self.articleSlug != null){
        articleFactory.getArticleBySlug(self.articleSlug, function (response) {
            if(response == null){
                self.articleNotFound = true;
                self.articles = [];
            } else{
                self.articles = [response];
            }
            setTimeout(bindTooltips, 100);
        }, function () { });
      } else{
          articleFactory.getArticles(self.filterTags, self.filterCategories, function (response) {
              self.articles = response;
              setTimeout(bindTooltips, 100);
          }, function () { });
      }
    }

    function reloadArticle(id) {

        articleFactory.getArticle(id, function (response) {
            var index = _.findIndex(self.articles, function (ar) { return ar.oid == id; });

            self.articles = _.filter(self.articles, function (ar) { return ar.oid != id; });

            self.articles.splice(index, 0, response);

            setTimeout(bindTooltips, 100);
        }, function () { });
    }

    function loadLoggedUser() {
        articleFactory.getLoggedUser(function (response) {
            if (response != "") {
                self.loggedUser = response;
            } else {
                self.loggedUser = null;
            }
        }, function () { });
    }

    function siginError(error, message) {
        self.signinError = error;
        if (!error) {
            self.signinMessage = "";
        } else {
            self.signinMessage = message;
        }
    }

    function showAlert(type, title, message, timeout) {
        self.globalMessageClass = type;
        self.globalMessageTitle = title;
        self.globalMessage = message;
        self.globalMessageShow = true;

        setTimeout(function () {
            self.globalMessageShow = false;
        }, timeout);
    }

    self.init = function () {
        var url = window.location.href;
        var arr = url.split("/");
        var domain = arr[0] + "//" + arr[2]

        var urlWithoutDomain = url.replace(domain + "/", "");
        var slashSplit = urlWithoutDomain.split("/");
        if(slashSplit[0].toLowerCase() == "posts" && slashSplit.length > 1){
            self.articleSlug = slashSplit[1];
        }
        loadCategories();
        loadArticles();
        loadLoggedUser();
    }

    self.logInModal = function () {
        showModal("loginModal");
    }

    self.signInModal = function () {
        showModal("signinModal");
    }

    self.deleteArticleModal = function(oid) {
        showModal("deleteArticleModal");
        self.selectedArticleOid = oid;
    }

    self.createArticleModal = function() {
		    self.isEditingArticle = false;
        showModal("createArticleModal");
    }

    self.createCategoryModal = function(){
      showModal("createCategoryModal");
    }

    self.login = function () {
        self.loginError = false;
        var loginInfo = {
            email: self.loginEmailInput,
            password: self.loginPasswordInput
        }

        articleFactory.loginUser(loginInfo, function (response) {
            if (response == null || response == "") {
                self.loginError = true;
            } else {
                self.loggedUser = response;
                $("#loginModal").modal("hide");
            }

        }, function() {
            showAlert("alert-danger", "Error", "An unknown error has occurred", 5000);
        });
    }

    self.logout = function () {
        articleFactory.logoutUser(function (response) {
            loadLoggedUser();
        }, function() {
            loadLoggedUser();
        });
    }

    self.signin = function() {
        self.signinError = false;

        if (self.signinPasswordInput != self.signinConfirmPasswordInput) {
            siginError(true, "Password and Password Confirmation do not match");
        }

        var signinInfo = {
            name: self.signinNameInput,
            email: self.signinEmailInput,
            password: self.signinPasswordInput
        }

        articleFactory.signinUser(signinInfo, function (response) {
            self.signinError = !response.success;
            if (response.success) {
                $("#signinModal").modal("hide");
                self.loginEmailInput = self.signinEmailInput;
                self.loginPasswordInput = self.signinPasswordInput;
                self.login();
            } else {
                self.signinMessage = response.message;
            }
        }, function () { });
    }

    self.deleteArticle = function() {
        articleFactory.deleteArticle(self.selectedArticleOid, function (response) {
            self.articles = _.filter(self.articles, function(article) {
                return article.oid != self.selectedArticleOid;
            });
            self.selectedArticleOid = "";
            hideModal("deleteArticleModal");
        }, function () {
            self.selectedArticleOid = "";
            hideModal("deleteArticleModal");
        });
    }

    self.createArticle = function() {
        var article = {};

        article.name = self.createArticleNameInput;
        article.slug = self.createArticleSlugInput;
        article.text = self.createArticleTextInput;
        article.tags = _.map(self.createArticleTagsInput.split(","), function (tag) { return { value: tag } });
        var categoryValue = $("#create-article-categories-input").val();
        article.categories =  categoryValue == "" ? [] :  [{value: categoryValue}]

  		if(self.isEditingArticle){
  			articleFactory.updateArticle(self.editingArticleID, article, function (response) {
  			self.createArticleError = !response.success;
  				if (response.success) {
  					$("#createArticleModal").modal("hide");
  					loadArticles();
  				} else {
  					self.createArticleMessage = response.message;
  				}
  			},
  			function () {
  				showAlert("alert-danger", "Error", "An unknown error has occurred", 5000);
  			});
  		} else{
          articleFactory.createArticle(article, function (response) {
              self.createArticleError = !response.success;
              if (response.success) {
                $("#createArticleModal").modal("hide");
                loadArticles();
              } else {
                self.createArticleMessage = response.message;
              }
            },
            function () {
            showAlert("alert-danger", "Error", "An unknown error has occurred", 5000);
          });
  		}
    }

    self.createArticleComment = function(articleID) {
        var text = $("textarea[input-oid=" + articleID + "]:first").val();
        var comment = { comment: text }

        articleFactory.createComment(articleID, comment, function(response) {
                reloadArticle(articleID);
            },
        function() {
            showAlert("alert-danger", "Error", "An unknown error has occurred", 5000);
        });
    }

    self.createCategory = function() {
        var category = {};
        category.value = self.createCategoryNameInput;

        articleFactory.createCategory(category, function(response) {
            self.createCategoryError = !response.success;
            if (response.success) {
              loadCategories();
            } else {
              self.createCategoryMessage = response.message;
            }
        },
        function() {
            showAlert("alert-danger", "Error", "An unknown error has occurred", 5000);
        });
    }

	self.editArticleModal = function(article){
		self.editingArticleID = article.oid
		self.isEditingArticle = true;
		self.createArticleNameInput = article.name;
        self.createArticleSlugInput = article.slug;
        self.createArticleTextInput = self.formatText(article.text);
        self.createArticleTagsInput = _.map(article.tags, function (tag) { return tag.value }).join(",");

        var articleCategory = article.categories.length > 0 ? article.categories[0].value : "";
         $("#create-article-categories-input").val(articleCategory);



		showModal("createArticleModal");
	}

  self.deleteCategory = function(oid){
    articleFactory.deleteCategory(oid, function(response) {
      loadCategories();
    },
    function() {
        showAlert("alert-danger", "Error", "An unknown error has occurred", 5000);
    });
  }

  self.filterArticles = function(){
    loadArticles();
  }

  self.filterTag = function(value){
    self.filterTags = value;
    self.hasFilterTags = true;
    loadArticles();
  }

  self.filterCategory = function(value){
    self.filterCategories = value;
    self.hasFilterCategories = true;
    loadArticles();
  }

  self.deleteTagFilter = function(){
    self.filterTags = "";
    self.hasFilterTags = false;
      loadArticles();
  }

  self.deleteCategoryFilter = function(){
    self.filterCategories = "";
    self.hasFilterCategories = false;
      loadArticles();
  }

  self.formatText = function(value){
    while(value.indexOf("<p>") >= 0){
      value = value.replace("<p>","\n");
    }
    return value;
  }
});
