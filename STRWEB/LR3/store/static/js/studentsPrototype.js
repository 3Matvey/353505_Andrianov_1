// Base class (Person)
function Person(name, surname) {
  this.name = name;
  this.surname = surname;
}

Person.prototype.getName = function() {
  return this.name;
};

Person.prototype.getSurname = function() {
  return this.surname;
};

Person.prototype.setName = function(name) {
  this.name = name;
};

Person.prototype.setSurname = function(surname) {
  this.surname = surname;
};

function Student(name, surname, schoolClass) {
  Person.call(this, name, surname);
  this.schoolClass = schoolClass;
}

// Set up prototype chain
Student.prototype = Object.create(Person.prototype);
Student.prototype.constructor = Student;

Student.prototype.getSchoolClass = function() {
  return this.schoolClass;
};

Student.prototype.setSchoolClass = function(schoolClass) {
  this.schoolClass = schoolClass;
};

Student.prototype.getFullInfo = function() {
  return `${this.name} ${this.surname}, класс ${this.schoolClass}`;
};

// StudentManager class
function StudentManager() {
  this.students = [];
}

StudentManager.prototype.addStudent = function(name, surname, schoolClass) {
  const student = new Student(name, surname, schoolClass);
  this.students.push(student);
  return student;
};

StudentManager.prototype.getAllStudents = function() {
  return this.students;
};

StudentManager.prototype.findDuplicateSurnames = function() {
  const surnameCount = {};
  
  this.students.forEach(student => {
    const surname = student.getSurname().toLowerCase();
    surnameCount[surname] = (surnameCount[surname] || 0) + 1;
  });
  
  const duplicates = Object.keys(surnameCount)
    .filter(surname => surnameCount[surname] > 1)
    .map(surname => ({
      surname: surname,
      count: surnameCount[surname],
      students: this.students.filter(s => s.getSurname().toLowerCase() === surname)
    }));
  
  return duplicates;
};

StudentManager.prototype.displayStudents = function(containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;
  
  container.innerHTML = '';
  
  if (this.students.length === 0) {
    container.innerHTML = '<p class="text-muted">Нет добавленных учеников</p>';
    return;
  }
  
  this.students.forEach((student, index) => {
    const studentEl = document.createElement('div');
    studentEl.className = 'list-group-item';
    studentEl.innerHTML = `
      <div class="d-flex justify-content-between align-items-center">
        <div>
          <strong>${student.getFullInfo()}</strong>
        </div>
        <button class="btn btn-sm btn-danger removeStudentBtn" data-index="${index}">Удалить</button>
      </div>
    `;
    container.appendChild(studentEl);
  });
};

StudentManager.prototype.displayDuplicates = function(containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;
  
  const duplicates = this.findDuplicateSurnames();
  
  if (duplicates.length === 0) {
    container.innerHTML = '<p class="text-success">Однофамильцев не найдено</p>';
    return;
  }
  
  let html = '<div class="alert alert-warning">';
  html += '<strong>Найдены однофамильцы:</strong><ul class="mt-2">';
  
  duplicates.forEach(dup => {
    html += `<li><strong>${dup.surname}</strong> (${dup.count} учеников):`;
    html += '<ul>';
    dup.students.forEach(student => {
      html += `<li>${student.getName()} ${student.getSurname()} - класс ${student.getSchoolClass()}</li>`;
    });
    html += '</ul></li>';
  });
  
  html += '</ul></div>';
  container.innerHTML = html;
};

// Initialize prototype variant
function initPrototypeVariant() {
  const prototypeManager = new StudentManager();
  
  // Add sample data
  prototypeManager.addStudent('Иван', 'Иванов', '9А');
  prototypeManager.addStudent('Петр', 'Петров', '8Б');
  prototypeManager.addStudent('Александр', 'Иванов', '10В');
  prototypeManager.addStudent('Мария', 'Сидорова', '9А');
  
  // Display initial data
  prototypeManager.displayStudents('prototypeStudentsList');
  prototypeManager.displayDuplicates('prototypeDuplicates');
  
  // Form submission
  const prototypeForm = document.getElementById('prototypeForm');
  if (prototypeForm) {
    prototypeForm.addEventListener('submit', function(e) {
      e.preventDefault();
      
      const name = document.getElementById('prototypeName').value.trim();
      const surname = document.getElementById('prototypeSurname').value.trim();
      const schoolClass = document.getElementById('prototypeClass').value.trim();
      
      if (name && surname && schoolClass) {
        prototypeManager.addStudent(name, surname, schoolClass);
        prototypeManager.displayStudents('prototypeStudentsList');
        prototypeManager.displayDuplicates('prototypeDuplicates');
        prototypeForm.reset();
      }
    });
  }
  
  // Remove student functionality
  const prototypeStudentsList = document.getElementById('prototypeStudentsList');
  if (prototypeStudentsList) {
    prototypeStudentsList.addEventListener('click', function(e) {
      if (e.target.classList.contains('removeStudentBtn')) {
        const index = parseInt(e.target.getAttribute('data-index'));
        prototypeManager.students.splice(index, 1);
        prototypeManager.displayStudents('prototypeStudentsList');
        prototypeManager.displayDuplicates('prototypeDuplicates');
      }
    });
  }
}

// Wait for DOM and initialize
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initPrototypeVariant);
} else {
  initPrototypeVariant();
}
