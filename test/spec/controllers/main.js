'use strict';

describe('Controller: MainCtrl', function () ***REMOVED***

  // load the controller's module
  beforeEach(module('setlistspyApp'));

  var MainCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) ***REMOVED***
    scope = $rootScope.$new();
    MainCtrl = $controller('MainCtrl', ***REMOVED***
      $scope: scope
      // place here mocked dependencies
    ***REMOVED***);
  ***REMOVED***));

  it('should attach a list of awesomeThings to the scope', function () ***REMOVED***
    expect(MainCtrl.awesomeThings.length).toBe(3);
  ***REMOVED***);
***REMOVED***);
