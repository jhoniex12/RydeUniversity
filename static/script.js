// Ryde University Student Records - JavaScript

// Show alert message
function showAlert(message, type = 'success') {
    const alertBox = document.getElementById('alertBox');
    alertBox.className = `alert alert-${type}`;
    alertBox.textContent = message;
    alertBox.style.display = 'block';
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        alertBox.style.display = 'none';
    }, 5000);
}

// Show Add Student Modal
function showAddStudentModal() {
    document.getElementById('modalTitle').textContent = 'Add New Student';
    document.getElementById('studentForm').reset();
    document.getElementById('studentId').value = '';
    document.getElementById('studentModal').style.display = 'block';
}

// Edit Student
async function editStudent(studentId) {
    try {
        const response = await fetch(`/api/students/${studentId}`);
        const data = await response.json();
        
        if (data.success) {
            const student = data.data;
            
            document.getElementById('modalTitle').textContent = 'Edit Student';
            document.getElementById('studentId').value = student.id;
            document.getElementById('name').value = student.name;
            document.getElementById('address').value = student.address;
            document.getElementById('city').value = student.city;
            document.getElementById('state').value = student.state;
            document.getElementById('email').value = student.email;
            document.getElementById('phone').value = student.phone;
            
            document.getElementById('studentModal').style.display = 'block';
        } else {
            showAlert('Error loading student data', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showAlert('Error loading student data', 'error');
    }
}

// Delete Student
function deleteStudent(studentId) {
    console.log('Delete button clicked for student ID:', studentId);
    
    if (!confirm('Are you sure you want to delete this student?')) {
        console.log('Delete cancelled by user');
        return;
    }
    
    console.log('Sending DELETE request for student ID:', studentId);
    
    fetch(`/api/students/${studentId}`, {
        method: 'DELETE'
    })
    .then(response => {
        console.log('Response status:', response.status);
        return response.json();
    })
    .then(data => {
        console.log('Response data:', data);
        
        if (data.success) {
            showAlert('Student deleted successfully', 'success');
            // Remove row from table
            const row = document.querySelector(`tr[data-id="${studentId}"]`);
            if (row) {
                row.remove();
            }
            
            // Reload page if no students left
            const tbody = document.getElementById('studentsTableBody');
            if (tbody.children.length === 0) {
                location.reload();
            }
        } else {
            showAlert(data.error || 'Error deleting student', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Error deleting student', 'error');
    });
}

// Close Modal
function closeModal() {
    document.getElementById('studentModal').style.display = 'none';
}

// Handle Form Submission
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('studentForm');
    
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const studentId = document.getElementById('studentId').value;
            const formData = {
                name: document.getElementById('name').value.trim(),
                address: document.getElementById('address').value.trim(),
                city: document.getElementById('city').value.trim(),
                state: document.getElementById('state').value.trim(),
                email: document.getElementById('email').value.trim(),
                phone: document.getElementById('phone').value.trim()
            };
            
            // Validate form data
            if (!formData.name || !formData.address || !formData.city || 
                !formData.state || !formData.email || !formData.phone) {
                showAlert('Please fill in all required fields', 'error');
                return;
            }
            
            try {
                let response;
                if (studentId) {
                    // Update existing student
                    response = await fetch(`/api/students/${studentId}`, {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(formData)
                    });
                } else {
                    // Add new student
                    response = await fetch('/api/students', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(formData)
                    });
                }
                
                const data = await response.json();
                
                if (data.success) {
                    showAlert(data.message, 'success');
                    closeModal();
                    
                    // Reload page to show updated data
                    setTimeout(() => {
                        location.reload();
                    }, 1000);
                } else {
                    showAlert(data.error || 'Error saving student', 'error');
                }
            } catch (error) {
                console.error('Error:', error);
                showAlert('Error saving student', 'error');
            }
        });
    }
    
    // Close modal when clicking outside of it
    window.onclick = function(event) {
        const modal = document.getElementById('studentModal');
        if (event.target === modal) {
            closeModal();
        }
    }
});

// Search students (client-side filter)
function searchStudents() {
    const input = document.getElementById('searchInput');
    const filter = input.value.toUpperCase();
    const table = document.getElementById('studentsTable');
    const tr = table.getElementsByTagName('tr');
    
    for (let i = 1; i < tr.length; i++) {
        let found = false;
        const td = tr[i].getElementsByTagName('td');
        
        for (let j = 0; j < td.length - 1; j++) { // Exclude actions column
            if (td[j]) {
                const txtValue = td[j].textContent || td[j].innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    found = true;
                    break;
                }
            }
        }
        
        tr[i].style.display = found ? '' : 'none';
    }
}
