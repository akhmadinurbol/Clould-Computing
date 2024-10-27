const express = require('express');
const multer = require('multer');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Set storage engine for multer
const storage = multer.diskStorage({
  destination: './uploads/',
  filename: (req, file, cb) => {
    cb(null, file.fieldname + '-' + Date.now() + path.extname(file.originalname));
  }
});

// Initialize upload variable
const upload = multer({
  storage: storage,
  limits: { fileSize: 1000000 }, // 1 MB limit
}).single('file'); // Expect a single file with the field name "file"

// Serve the uploads folder statically
app.use('/uploads', express.static('uploads'));

// Route to upload a file
app.post('/upload', (req, res) => {
  upload(req, res, (err) => {
    if (err) {
      return res.status(400).send('File upload failed.');
    }
    res.send(`File uploaded successfully: <a href="/uploads/${req.file.filename}">View File</a>`);
  });
});

// Route to test the server
app.get('/', (req, res) => {
  res.send(`
    <h2>File Sharing Application</h2>
    <form action="/upload" method="POST" enctype="multipart/form-data">
      <input type="file" name="file" required />
      <button type="submit">Upload File</button>
    </form>
  `);
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
