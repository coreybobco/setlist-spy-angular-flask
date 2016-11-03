'use strict';

/**
 * @ngdoc function
 * @name markovmutatorApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the markovmutatorApp
 */
angular.module('markovmutatorApp')
  .controller('MutagenCtrl', function ($scope, $http) ***REMOVED***
    $scope.genes = [];
    $scope.addGene = function(url) ***REMOVED***
      var url = (url) ? JSON.stringify(url) : JSON.stringify(document.querySelector("#url").value);
      $http.post('/addGene', url)
      .then(function successCallback(response) ***REMOVED***
        document.querySelector("#mutate_button").disabled = false;
        var gene = response.data;
        var duplicate_found = false;
        for(var i = 0; i < $scope.genes.length; i++) ***REMOVED***
          if (gene.source == $scope.genes[i].source && gene.document_id == $scope.genes[i].document_id) ***REMOVED***
            duplicate_found = true;
            break;
          ***REMOVED***
        ***REMOVED***
        if (!duplicate_found) ***REMOVED***
          $scope.genes.push(gene);
        ***REMOVED***
      ***REMOVED***, function errorCallback(response) ***REMOVED***
        console.log("Error\n" + response)
      ***REMOVED***);
    ***REMOVED***;
    $scope.mutate = function() ***REMOVED***
      var mutate_button = $("#mutate_button");
      var options = ***REMOVED******REMOVED***;
      options.genes = [];
      for(var i = 0; i < $scope.genes.length; i++) ***REMOVED***
        if (document.querySelector("#checkbox_gene_" + i.toString()).checked) ***REMOVED***
          options.genes.push($scope.genes[i]);
        ***REMOVED***
      ***REMOVED***
      if (options.genes.length > 0) ***REMOVED***
        mutate_button.disabled = true;
        mutate_button.css('color', 'gray');
        options.purge_mode = $("#purge_mode").is(':checked');
        options.purge_ratio = $("#purge_ratio").val();
        options.block_length = $("input:checked[name=block_length]")[0].value;
        options = JSON.stringify(options);
        $http.post('mutate', options)
          .then(function successCallback(response) ***REMOVED***
            var booklet = $("#mutant_book").booklet(***REMOVED***width: '900px', height: '520px', pageTotal: 15***REMOVED***);
            var output = response.data;
            var page_texts = output.match(/.***REMOVED***1,1400***REMOVED***[\s$]/g);
            $("#page1").find('p').text(page_texts[1]);
            for (i=0; i < page_texts.length; i++) ***REMOVED***
              $("#page" + i.toString()).find('p').text(page_texts[i]);
            ***REMOVED***
            mutate_button.css('color', 'black');
            mutate_button.disabled = false;
          ***REMOVED***,
            function errorCallback(response) ***REMOVED***
            console.log("Error\n" + response)
        ***REMOVED***);
      ***REMOVED*** else ***REMOVED***

      ***REMOVED***
    ***REMOVED***;
    $scope.deleteGene = function(gene)***REMOVED***
      var index = $scope.genes.indexOf(gene);
      $scope.genes.splice(index, 1);
    ***REMOVED***;
  ***REMOVED***);
