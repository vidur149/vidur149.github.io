(function() {
    angular.module("todo", []);
    angular.module("todo").controller("myCtrl", myCtrl);
    myCtrl.$inject = ['$http'];

    function myCtrl($http) {
        var self = this;
        self.tasks = []
        self.title;
        $http.get('http://localhost:5000/tasks').then(function(response) {
            self.tasks = response.data['tasks'];
        });

        self.removeTask = function(id) {
            for (let i = 0; i < self.tasks.length; i++) {
                if (self.tasks[i]['id'] === id) {
                    if (i > -1) {
                        self.tasks.splice(i, 1);
                    }
                    break;
                }
            }
            $http.delete('http://localhost:5000/tasks/' + id);
        };

        self.addTask = function() {
            if (self.title !== "") {
                jsObj = {
                    title: self.title
                };
                self.title = "";
                let jsonObj = JSON.stringify(jsObj);
                $http.post('http://localhost:5000/tasks', jsonObj).then(function() {
                    $http.get('http://localhost:5000/tasks').then(function(response) {
                        self.tasks = response.data['tasks'];
                    });
                });
            }
        };
    }
})();