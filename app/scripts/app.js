'use strict';

/**
 * @ngdoc overview
 * @name markovmutatorApp
 * @description
 * # markovmutatorApp
 *
 * Main module of the application.
 */
angular
  .module('markovmutatorApp', [
    'ngAnimate',
    'ngMessages',
    'ngResource',
    'ngRoute',
    'ngSanitize'
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
