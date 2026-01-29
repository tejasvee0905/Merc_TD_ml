document.getElementById('loanForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // Get form data
    const formData = {
        married: document.getElementById('married').value,
        education: document.getElementById('education').value,
        selfEmployed: document.getElementById('selfEmployed').value,
        applicantIncome: document.getElementById('applicantIncome').value,
        coapplicantIncome: document.getElementById('coapplicantIncome').value,
        loanAmount: document.getElementById('loanAmount').value,
        loanTerm: document.getElementById('loanTerm').value,
        creditHistory: document.getElementById('creditHistory').value,
        propertyArea: document.getElementById('propertyArea').value
    };
    
    // Show loader
    const submitBtn = document.getElementById('submitBtn');
    const btnText = document.getElementById('btnText');
    const btnLoader = document.getElementById('btnLoader');
    
    submitBtn.disabled = true;
    btnText.style.display = 'none';
    btnLoader.style.display = 'inline-block';
    
    // Hide previous results
    document.getElementById('resultSection').style.display = 'none';
    
    try {
        // Call API
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            displayResult(result);
        } else {
            alert('Error: ' + result.error);
        }
        
    } catch (error) {
        alert('Error connecting to server: ' + error.message);
    } finally {
        // Hide loader
        submitBtn.disabled = false;
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    }
});

function displayResult(result) {
    const resultSection = document.getElementById('resultSection');
    const resultCard = document.getElementById('resultCard');
    const resultTitle = document.getElementById('resultTitle');
    const resultMessage = document.getElementById('resultMessage');
    const approvalBar = document.getElementById('approvalBar');
    const rejectionBar = document.getElementById('rejectionBar');
    const approvalPercent = document.getElementById('approvalPercent');
    const rejectionPercent = document.getElementById('rejectionPercent');
    const confidence = document.getElementById('confidence');
    
    // Set result status
    if (result.status === 'approved') {
        resultCard.className = 'result-card approved';
        resultTitle.textContent = '✅ Loan Approved!';
        resultMessage.textContent = 'Congratulations! Your loan application has been approved based on the provided information.';
    } else {
        resultCard.className = 'result-card rejected';
        resultTitle.textContent = '❌ Loan Rejected';
        resultMessage.textContent = 'Unfortunately, your loan application was not approved. Please review your information and try again.';
    }
    
    // Set probability bars
    approvalBar.style.width = result.probability.approval + '%';
    rejectionBar.style.width = result.probability.rejection + '%';
    
    approvalPercent.textContent = result.probability.approval + '%';
    rejectionPercent.textContent = result.probability.rejection + '%';
    
    confidence.textContent = result.confidence + '%';
    
    // Show result section with animation
    resultSection.style.display = 'block';
    
    // Smooth scroll to results
    setTimeout(() => {
        resultSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 100);
}

// Add input validation
document.getElementById('applicantIncome').addEventListener('input', function() {
    if (this.value < 0) this.value = 0;
});

document.getElementById('coapplicantIncome').addEventListener('input', function() {
    if (this.value < 0) this.value = 0;
});

document.getElementById('loanAmount').addEventListener('input', function() {
    if (this.value < 0) this.value = 0;
});
