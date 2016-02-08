var app = app || angular.module('FlaskMessages', ['ngMaterial', 'ngResource']);
    //Config theme
app.config(function($mdThemingProvider, $mdIconProvider) {
  $mdThemingProvider.theme('default').primaryPalette('blue-grey', {'default': '600'}).accentPalette('brown', {'default': '700'});

  $mdIconProvider
    .icon("menu",          '/static/img/menu.svg', 24)
    .icon("account",       '/static/img/account.svg', 24)
    .icon("facebook",      '/static/img/facebook.svg', 24)
    .icon("google",        '/static/img/google.svg', 24)
    .icon("twitter",       '/static/img/twitter.svg', 24)
    .icon("home",          '/static/img/home.svg', 24)
    .icon("friends",       '/static/img/friends.svg', 24)
    .icon("logout",        '/static/img/logout.svg', 24)
    .icon("login",         '/static/img/login.svg', 24)
    .icon("group",         '/static/img/group.svg', 24)
    .icon("info",          '/static/img/info.svg', 24)
    .icon("reply",         '/static/img/reply.svg', 24)
    .icon("settings",      '/static/img/settings.svg', 24)
    .icon("empty-user",    '/static/img/empty-user.svg', 24)
    .icon("filled-user",   '/static/img/filled-user.svg', 24)
    .icon("notification",  '/static/img/notification-bell.svg', 24)
    .icon("password",      '/static/img/password.svg', 24)
    .icon("right-arrow",   '/static/img/right-arrow.svg', 24)
    .icon("upload",        '/static/img/share-upload.svg', 24)
    .icon("clear",         '/static/img/clear.svg', 24)
    .icon("refresh",       '/static/img/refresh.svg', 24)
    .icon("add",           '/static/img/add.svg', 24)
    .icon("add-2",         '/static/img/add-2.svg', 24)
    .icon("cloud",         '/static/img/cloud.svg', 24)
    .icon("chat-two-line", '/static/img/chat-two-line.svg', 24);
});

app.factory('Author', function($resource, $cacheFactory) {
    /*
     * Author factory is primarily take advantage of
     * in situations where we need to display a lot of duplicate
     * API information that we might as well cache instead of reach
     * out of every single time. This is especially useful if all
     * of this is happening in a very short period of time so we
     * can be assured the data is not going to change and we can
     * lighten the API data transaction load
     *
     * $resource supports caching by itself, so we just have to pass
     * in a homemade $cacheFactory, or let it make a default one of $http cache
     */
    var authorCache = $cacheFactory('Author');
    return {
    	get: function(id) {
    		console.log(authorCache);
    		return $resource('/getUserDataFromId/:id', {id: id}, {'get': {method:'GET', cache: authorCache}}).get();
    	}
    }
});

app.filter('timestampToDate', function () {
    return function (timestamp) {
    	var span = Date.now() - timestamp*1000;
    	var retVal = "";
    	switch (true) {
    		case span<30000:  // 30 seconds
    			retVal = "just now";
    			break;
    		case span<60000:  // 1 mins
    			retVal = "1 minute ago";
    			break;
    		case span<120000: // 2 mins
    			retVal = "2 minutes ago";
    			break;
    		case span<126000: // 2 mins
    			retVal = "3 minutes ago";
    			break;
    		case span<180000: // 3 mins
    			retVal = "3 minutes ago";
    			break;
    		case span<240000: // 4 mins
    			retVal = "4 minutes ago";
    			break;
    		case span<300000: // 5 mins
    			retVal = "5 minutes ago";
    			break;
    		case span<360000: // 6 mins
    			retVal = "6 minutes ago";
    			break;
    		case span<420000: // 7 mins
    			retVal = "7 minutes ago";
    			break;
    		case span<480000: // 8 mins
    			retVal = "8 minutes ago";
    			break;
    		case span<540000: // 9 mins
    			retVal = "9 minutes ago";
    			break;
    		case span<600000: // 10 mins
    			retVal = "10 minutes ago";
    			break;
    		case span<8640000000: // 1 day
    			retVal = (new Date(timestamp*1000).toString("hh:mm tt"));
    			break;
    		default:
    			var date = (new Date(timestamp*1000));
    			var time = date.toString("hh:mm tt");
    			var dateString = ('0' + (date.getMonth() + 1)).slice(-2) + '-' + ('0' + date.getDate()).slice(-2) + '-' + date.getFullYear();
    			retVal = time + " " + dateString;
    	}
        return retVal;
    };
});