var app = angular.module("todo-app", []);

app.controller("TodoCtrl", function($scope) {

    $scope.todos = [{
        text: 'Learn AngularJS',
        done: false
    }, {
        text: 'Build an app',
        done: false
    }];

    $scope.todoText = '';

    $scope.getLeftTodos = function() {
        var count = 0;
        for (var i = 0; i < $scope.todos.length; i++) {
            console.log($scope.todos[i]);
            if ($scope.todos[i].done === false) {
                count++;
            }
        }
        return count;
    };

    $scope.addTodo = function() {
        if ($scope.todoText !== '') {
            $scope.todos.push({
                text: $scope.todoText,
                done: false
            });
            $scope.todoText = '';
        };
    };

    $scope.changeState = function(todo) {
        todo.done = todo.done ? false : true;
    };

});