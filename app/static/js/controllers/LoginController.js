app.controller('LoginController', function($scope, $http, $timeout, $mdToast, $animate) {
  
  // Initilization
  $scope.loginLinks = $scope.loginLinks || {};

    $scope.redirect = function(url) {
    	window.location = "/.."+url;
    }

});