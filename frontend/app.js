// ===== CONFIGURATION =====
const API_BASE_URL = 'http://localhost:5000';
const API_ENDPOINTS = {
    health: `${API_BASE_URL}/health`,
    caption: `${API_BASE_URL}/caption`,
    modelInfo: `${API_BASE_URL}/models/info`
};

// ===== STATE MANAGEMENT =====
let currentFile = null;
let serverOnline = false;

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    checkServerStatus();
    // Check server status every 10 seconds
    setInterval(checkServerStatus, 10000);
});

// ===== EVENT LISTENERS =====
function initializeEventListeners() {
    const fileInput = document.getElementById('fileInput');
    const uploadArea = document.getElementById('uploadArea');

    // File input change
    fileInput.addEventListener('change', handleFileSelect);

    // Drag and drop events
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);

    // Click on upload area
    uploadArea.addEventListener('click', () => fileInput.click());
}

// ===== SERVER STATUS CHECK =====
async function checkServerStatus() {
    const statusElement = document.getElementById('serverStatus');
    const detailElement = document.getElementById('serverDetail');

    try {
        const response = await fetch(API_ENDPOINTS.health);
        const data = await response.json();

        if (data.status === 'healthy') {
            serverOnline = true;
            statusElement.textContent = '🟢 Online';
            statusElement.className = 'status-online';
            detailElement.textContent = 'Models loaded';
        } else {
            serverOnline = true;
            statusElement.textContent = '🟡 Degraded';
            statusElement.className = '';
            detailElement.textContent = 'Models not loaded';
        }
    } catch (error) {
        serverOnline = false;
        statusElement.textContent = '🔴 Offline';
        statusElement.className = 'status-offline';
        detailElement.textContent = 'Server không khả dụng';
        console.error('Server check failed:', error);
    }
}

// ===== DRAG & DROP HANDLERS =====
function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.add('drag-over');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.remove('drag-over');
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.remove('drag-over');

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

// ===== FILE HANDLING =====
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        handleFile(file);
    }
}

function handleFile(file) {
    // Validate file type
    const validTypes = ['image/jpeg', 'image/png', 'image/jpg'];
    if (!validTypes.includes(file.type)) {
        showError('Vui lòng chọn file ảnh (JPG, PNG)');
        return;
    }

    // Validate file size (10MB)
    const maxSize = 10 * 1024 * 1024;
    if (file.size > maxSize) {
        showError('File quá lớn. Vui lòng chọn file nhỏ hơn 10MB');
        return;
    }

    currentFile = file;
    displayPreview(file);
    processImage(file);
}

// ===== IMAGE PREVIEW =====
function displayPreview(file) {
    const reader = new FileReader();
    
    reader.onload = (e) => {
        const previewImage = document.getElementById('previewImage');
        const imageInfo = document.getElementById('imageInfo');
        const resultsSection = document.getElementById('resultsSection');

        previewImage.src = e.target.result;
        
        // Display file info
        const fileSizeMB = (file.size / (1024 * 1024)).toFixed(2);
        imageInfo.innerHTML = `
            <strong>Tên file:</strong> ${file.name}<br>
            <strong>Kích thước:</strong> ${fileSizeMB} MB<br>
            <strong>Định dạng:</strong> ${file.type}
        `;

        resultsSection.style.display = 'block';
        
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    };

    reader.readAsDataURL(file);
}

// ===== IMAGE PROCESSING =====
async function processImage(file) {
    if (!serverOnline) {
        showError('Server không khả dụng. Vui lòng kiểm tra lại kết nối.');
        return;
    }

    // Show loading state
    showLoading();

    try {
        // Create FormData
        const formData = new FormData();
        formData.append('file', file);
        formData.append('method', 'beam_search'); // Sử dụng Beam Search với k=3

        // Animate loading steps
        animateLoadingSteps();

        // Call API
        const response = await fetch(API_ENDPOINTS.caption, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Lỗi khi xử lý ảnh');
        }

        const result = await response.json();
        displayResults(result);

    } catch (error) {
        console.error('Error processing image:', error);
        showError(error.message || 'Đã xảy ra lỗi khi xử lý ảnh. Vui lòng thử lại.');
    }
}

// ===== LOADING ANIMATION =====
function showLoading() {
    document.getElementById('loadingState').style.display = 'block';
    document.getElementById('captionResults').style.display = 'none';
    document.getElementById('errorState').style.display = 'none';
}

function animateLoadingSteps() {
    const steps = [
        '✓ Tiền xử lý ảnh',
        '✓ Trích xuất đặc trưng',
        '⏳ Sinh chú thích với Beam Search...'
    ];
    
    let currentStep = 0;
    const interval = setInterval(() => {
        if (currentStep < steps.length) {
            const stepsHtml = steps.slice(0, currentStep + 1)
                .map(step => `<span class="step">${step}</span>`)
                .join('<br>');
            document.getElementById('loadingSteps').innerHTML = stepsHtml;
            currentStep++;
        } else {
            clearInterval(interval);
        }
    }, 800);
}

// ===== DISPLAY RESULTS =====
function displayResults(result) {
    // Hide loading
    document.getElementById('loadingState').style.display = 'none';
    document.getElementById('captionResults').style.display = 'block';

    // Display main caption
    document.getElementById('mainCaption').textContent = result.caption;

    // Display metadata
    const methodText = result.method === 'beam_search' 
        ? `Beam Search (k=${result.beam_width || 3})` 
        : 'Greedy Search';
    document.getElementById('method').textContent = methodText;
    document.getElementById('inferenceTime').textContent = `${result.inference_time}s`;

    // Display alternative captions (nếu có)
    if (result.all_captions && result.all_captions.length > 1) {
        const altCaptionsDiv = document.getElementById('alternativeCaptions');
        const altCaptionsList = document.getElementById('altCaptionsList');
        
        altCaptionsDiv.style.display = 'block';
        altCaptionsList.innerHTML = result.all_captions
            .map((item, index) => `
                <li>
                    <strong>#${index + 1}</strong> (Score: ${item.normalized_score.toFixed(3)}): 
                    ${item.caption}
                </li>
            `)
            .join('');
    } else {
        document.getElementById('alternativeCaptions').style.display = 'none';
    }

    // Success animation
    const captionCard = document.querySelector('.caption-card');
    captionCard.style.animation = 'fadeIn 0.5s ease-out';
}

// ===== ERROR HANDLING =====
function showError(message) {
    document.getElementById('loadingState').style.display = 'none';
    document.getElementById('captionResults').style.display = 'none';
    document.getElementById('errorState').style.display = 'block';
    document.getElementById('errorMessage').textContent = message;
}

// ===== UTILITY FUNCTIONS =====
function copyCaption() {
    const caption = document.getElementById('mainCaption').textContent;
    
    navigator.clipboard.writeText(caption).then(() => {
        // Show success feedback
        const btn = event.target;
        const originalText = btn.textContent;
        btn.textContent = '✓ Đã sao chép!';
        btn.style.background = '#27ae60';
        
        setTimeout(() => {
            btn.textContent = originalText;
            btn.style.background = '';
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy:', err);
        alert('Không thể sao chép. Vui lòng thử lại.');
    });
}

function resetApp() {
    // Reset file input
    document.getElementById('fileInput').value = '';
    currentFile = null;

    // Hide results section
    document.getElementById('resultsSection').style.display = 'none';

    // Reset states
    document.getElementById('loadingState').style.display = 'none';
    document.getElementById('captionResults').style.display = 'none';
    document.getElementById('errorState').style.display = 'none';

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ===== CONSOLE GREETING =====
console.log(`
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   🖼️  IMAGE CAPTIONING APPLICATION - LSTM-CNN            ║
║                                                           ║
║   Backend API: ${API_BASE_URL}                 ║
║   Status: Ready                                           ║
║                                                           ║
║   📚 Đồ án môn Python                                     ║
║   🎯 Tự động tạo chú thích cho ảnh                       ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
`);
