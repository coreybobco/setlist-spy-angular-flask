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
      .otherwise(***REMOVED***
        redirectTo: '/'
      ***REMOVED***);
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
