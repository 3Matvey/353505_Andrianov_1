// Variant 2: Class-based inheritance (ES6)

// Base class (Person)
class Person {
  constructor(name, surname) {
    this.name = name;
    this.surname = surname;
  }

  getName() {
    return this.name;
  }

  getSurname() {
    return this.surname;
  }

  setName(name) {
    this.name = name;
  }

  setSurname(surname) {
    this.surname = surname;
  }
}

// Child class (Student) - extends Person
class Student extends Person {
  constructor(name, surname, schoolClass) {
    super(name, surname);
    this.schoolClass = schoolClass;
  }

  getSchoolClass() {
    return this.schoolClass;
  }

  setSchoolClass(schoolClass) {
    this.schoolClass = schoolClass;
  }

  getFullInfo() {
    return `${this.name} ${this.surname}, класс ${this.schoolClass}`;
  }
}

// StudentManager class
class StudentManager {
  constructor() {
    this.students = [];
  }

  addStudent(name, surname, schoolClass) {
    const student = new Student(name, surname, schoolClass);
    this.students.push(student);
    return student;
  }

  getAllStudents() {
    return this.students;
  }

  findDuplicateSurnames() {
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
  }

  displayStudents(containerId) {
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
  }

  displayDuplicates(containerId) {
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
  }
}

// Initialize class variant
function initClassVariant() {
  const classManager = new StudentManager();
  
  // Add sample data
  classManager.addStudent('Иван', 'Иванов', '9А');
  classManager.addStudent('Петр', 'Петров', '8Б');
  classManager.addStudent('Александр', 'Иванов', '10В');
  classManager.addStudent('Мария', 'Сидорова', '9А');
  
  // Display initial data
  classManager.displayStudents('classStudentsList');
  classManager.displayDuplicates('classDuplicates');
  
  // Form submission
  const classForm = document.getElementById('classForm');
  if (classForm) {
    classForm.addEventListener('submit', function(e) {
      e.preventDefault();
      
      const name = document.getElementById('className').value.trim();
      const surname = document.getElementById('classSurname').value.trim();
      const schoolClass = document.getElementById('classClass').value.trim();
      
      if (name && surname && schoolClass) {
        classManager.addStudent(name, surname, schoolClass);
        classManager.displayStudents('classStudentsList');
        classManager.displayDuplicates('classDuplicates');
        classForm.reset();
      }
    });
  }
  
  // Remove student functionality
  const classStudentsList = document.getElementById('classStudentsList');
  if (classStudentsList) {
    classStudentsList.addEventListener('click', function(e) {
      if (e.target.classList.contains('removeStudentBtn')) {
        const index = parseInt(e.target.getAttribute('data-index'));
        classManager.students.splice(index, 1);
        classManager.displayStudents('classStudentsList');
        classManager.displayDuplicates('classDuplicates');
      }
    });
  }
}

// Wait for DOM and initialize
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initClassVariant);
} else {
  initClassVariant();
}
