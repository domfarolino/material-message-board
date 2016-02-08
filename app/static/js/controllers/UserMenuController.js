app.controller('UserMenuController', function($scope, $http, $animate, $mdDialog) {
  
  var originatorEv;
  $scope.openMenu = function($mdOpenMenu, ev) {
    originatorEv = ev;
    $mdOpenMenu(ev);
  };
  this.notificationsEnabled = true;
  $scope.toggleNotifications = function() {
    this.notificationsEnabled = !this.notificationsEnabled;
  };
  $scope.go = function(place) {
    window.location = "../"+place;
    /*for md-dialog: https://material.angularjs.org/latest/demo/menu*/
  };
  
});