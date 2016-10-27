'use strict';

/**
 * @ngdoc overview
 * @name markovmutatorApp
 * @description
 * # markovmutatorApp
 *
 * Main module of the application.
 */
var myApp = angular
  .module('markovmutatorApp', [
    'ngAnimate',
    'ngMessages',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'thatisuday.ng-image-gallery'
  ])
  .config(function ($routeProvider) ***REMOVED***
    $routeProvider
      .when('/', ***REMOVED***
        templateUrl: 'views/main.html',
        controller: 'MainCtrl',
        controllerAs: 'main'
      ***REMOVED***)
      .when('/about', ***REMOVED***
        templateUrl: 'views/about.html',
        controller: 'AboutCtrl',
        controllerAs: 'about'
      ***REMOVED***)
      .when('/images', ***REMOVED***
        templateUrl: 'views/images.html',
        controller: 'ImageCtrl',
        controllerAs: 'image',
        activetab: 'images'
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
