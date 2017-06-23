(function() {
    angular.module("todo", ['angularMoment']);
    angular.module("todo").controller("myCtrl", myCtrl);
    myCtrl.$inject = ['$http'];

    function myCtrl($http) {
        var self = this;
        self.tasks = [];
        self.title;

        $http.get('http://localhost:3000/tasks').then(function(response) {
            self.tasks = response.data;
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
            $http.delete('http://localhost:3000/tasks/' + id);
        };

        self.addTask = function() {
            if (self.title !== "") {
                var len = self.tasks.length;
                var id;
                id = len === 0 ? 0 : self.tasks[len - 1]['id'] + 1;
                var task = {
                    'title': self.title,
                    'id': id,
                    'createdDate': new Date()
                };
                let jsonObj = JSON.stringify(task);
                $http.post('http://localhost:3000/tasks', jsonObj).then(function() {
                    self.tasks.push(task);
                    self.title = '';
                });

            }
        };

        self.order = '';
        self.orderByDate = function() {
            self.order = self.order == 'title' ? '' : 'title';
        };
    }
})();