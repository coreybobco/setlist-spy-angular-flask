'use strict';

/**
 * @ngdoc overview
 * @name setlistspyApp
 * @description
 * # setlistspyApp
 *
 * Main module of the application.
 */
var myApp = angular
  .module('setlistspyApp', [
    'ngAnimate',
    'ngAria',
    'ngMaterial',
    'ngMessages',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'ui.grid'
  ])
  .config(function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/setlistspy.html',
        controller: 'SetlistSpyCtrl',
        controllerAs: 'setlistspy'
      })
      .otherwise({
        redirectTo: '/'
      });
  }).controller('HeaderCtrl', function HeaderController($scope, $location)
  {
    $scope.isActive = function (viewLocation) {
      return viewLocation === $location.path();
    };
  });

myApp.filter('range', function() {
  return function(input, total) {
    total = parseInt(total);

    for (var i=0; i<total; i++) {
      input.push(i);
    }

    return input;
  };
});
