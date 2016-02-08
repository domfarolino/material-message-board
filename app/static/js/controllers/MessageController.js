app.controller('MessagesController', function($scope, $http, $resource, $cacheFactory, Author, $timeout, $mdToast, $animate) {
    // Some initializers
    $scope.messages = $scope.messages || [];          // Local messages array will be populated filled with message objects from a successfull response of the api
    $scope.selectedAll = $scope.selectedAll || false; // Boolean tracking select/unselect all checkbox's state
    $scope.selected = $scope.selected || [];          // Array to hold id's of messages that are selected
    $scope.authorData = $scope.authorData || {};      // No longer in use, only used for old method of author retrieval
    
    $scope.getData = function() {
        $http.get('/api/messages').
            then(function(response) {
                if(angular.toJson(response.data.messages) != angular.toJson($scope.messages)) {
                    $scope.messages = response.data.messages;
                    $scope.clearAllSelected();
                    $scope.confirmRestOperation(response);
                }
            }, function(response) {
                $scope.messages = [];
                $scope.confirmRestOperation(response);
            });
    };

    $scope.messageInit = function(id) {
        // Things to do when a message is initialized;
        $scope.setAuthorDataFromAuthorId(id);
        $scope.keepMessagesScrolledDown();
    }

    $scope.keepMessagesScrolledDown = function() {
        var chatBox = document.getElementById('chat-box');
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    $scope.setAuthorDataFromAuthorId = function(id) {
        /*
         * See Author factory for REST caching purposes
         * So if there are hundreds of messages but only
         * 10 authors, I am only access the rest API 10 times
         * This is the main practical use for factories in this
         * application, where we need to fulfill many front-end
         * operations with a REST value we assume won't be changing
         * in the amount of time it takes to perform all of our
         * large numbered quick operations with the cached data
        */
        
        if(id in $scope.authorData) return;
        console.log($scope.authorData);
        $scope.authorData[id] = Author.get(id);

        /*
         * The below way to handle the cache is not bad. There
         * are some issues however. Whether or not cache is enabled
         * $http.get() service has problems returnig asynchronous data
         * conditionally
         */
        
        /*
        if(id in $scope.authorData) return;
        console.log($scope.authorData);
        console.log("setAuthorFromAuthorId has been called");
        $http.get('/getUserDataFromId/'+id, {cache: true}).then(function(response) {
            console.log(response.data);
            console.log($scope.authorData);
            $scope.authorData[id] = response.data;
        }, function(response) {
            console.log(response.data);
            console.log($scope.authorData);
            $scope.authorData = {};
        }).finally(function() {
            console.log("setAuthorFromAuthorId has been completed");
        });
*/

    };

    // Function to replicate setInterval using $timeout service.
    $scope.intervalFunction = function() {
        $timeout(function() {
            if(!$scope.autoUpdateCheck){
                $scope.getData();
            } else {
                $scope.getData();
                $scope.intervalFunction();
            }
        }, 1000);
    };

    $scope.addMessage = function() {
        var data = {"message": $scope.msgmsg};

        $http.post('/addMessage', data, {'Content-Type': 'application/json'}).
            then(function(response) {
                $scope.confirmRestOperation(response);
            }, function(response) {
                $scope.confirmRestOperation(response);
            });
        $scope.msgmsg = "";
    };

    $scope.deleteMessages = function() {
        var data = {id: $scope.selected};
        
        $http.post('/deleteMessage', data, {'Content-Type': 'application/json'}).
            then(function(response) {
                $scope.confirmRestOperation(response);
                $scope.clearAllSelected();
            }, function(response) {
                $scope.confirmRestOperation(response);
            });

    };

    $scope.toggleAll = function () {
        if ($scope.selectedAll == true) {
            $scope.clearAllSelected();
        } else if($scope.selectedAll == false) {
            $scope.populateAllSelected();
        }
    };

    $scope.clearAllSelected = function() {
        $scope.selected = [];
        $scope.selectedAll = false;
    };

    $scope.populateAllSelected = function() {
        $scope.clearAllSelected();
        for (var i = $scope.messages.length - 1; i >= 0; i--) {
            $scope.selected.push($scope.messages[i].id)
        };
        if($scope.messages.length == $scope.selected.length) $scope.selectedAll = true; // quick redundancy check before assigning selectedAll to true
    };

    $scope.returnAllSelected = function() {
        return $scope.selectedAll == true;
    };

    $scope.returnMessagesEmpty = function() {
        return $scope.messages.length == 0;
    }

    $scope.toggle = function(item, list) {
        var idx = list.indexOf(item);
        if (idx > -1) {
            list.splice(idx, 1);
        } else {
            list.push(item);
        }

        if($scope.messages.length == $scope.selected.length) {
            $scope.selectedAll = true;
        } else {
            $scope.selectedAll = false;
        }
    };

    $scope.exists = function(item, list) {
        return list.indexOf(item) > -1;
    };

    $scope.confirmRestOperation = function(response) {
        $scope.showActionToast(response.statusText);
    };

    $scope.toastPosition = {
        bottom: true,
        top: false,
        left: true,
        right: false
    };

    $scope.getToastPosition = function() {
        return Object.keys($scope.toastPosition)
        .filter(function(pos) { return $scope.toastPosition[pos]; })
        .join(' ');
    };

    $scope.showActionToast = function(data) {
        var toast = $mdToast.simple()
        .content(data)
        .action('OK')
        .highlightAction(false)
        .position($scope.getToastPosition());
        $mdToast.show(toast).then(function(response) {
        });
    };
    //$scope.autoUpdateCheck = true;
    //$scope.intervalFunction();
});