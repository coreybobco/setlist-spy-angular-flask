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
  .config(function ($routeProvider) ***REMOVED***
    $routeProvider
      .when('/', ***REMOVED***
        templateUrl: 'views/setlistspy.html',
        controller: 'SetlistSpyCtrl',
        controllerAs: 'setlistspy'
      ***REMOVED***)
      .otherwise(***REMOVED***
        redirectTo: '/'
      ***REMOVED***);
  ***REMOVED***).controller('HeaderCtrl', function HeaderController($scope, $location)
  ***REMOVED***
    $scope.isActive = function (viewLocation) ***REMOVED***
      return viewLocation === $location.path();
    ***REMOVED***;
  ***REMOVED***);

myApp.filter('range', function() ***REMOVED***
  return function(input, total) ***REMOVED***
    total = parseInt(total);

    for (var i=0; i<total; i++) ***REMOVED***
      input.push(i);
    ***REMOVED***

    return input;
  ***REMOVED***;
***REMOVED***);
