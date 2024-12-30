// const express = require("express");
// const multer = require("multer");
// const { google } = require("googleapis");
// const fs = require("fs");
// const path = require("path");
// const bodyParser = require("body-parser");

// const app = express();
// const port = 3001;

// app.use(bodyParser.json());
// app.use(bodyParser.urlencoded({ extended: true }));

// const upload = multer({ dest: "uploads/" });



// const oauth2Client = new google.auth.OAuth2(
//   CLIENT_ID,
//   CLIENT_SECRET,
//   REDIRECT_URI
// );

// app.get("/auth", (req, res) => {
//   const authUrl = oauth2Client.generateAuthUrl({
//     access_type: "online",
//     scope: SCOPES,
//   });
//   res.redirect(authUrl);
// });

// // Handle OAuth2 callback
// app.get("/oauth2callback", async (req, res) => {
//   const { code } = req.query;
//   try {
//     const { tokens } = await oauth2Client.getToken(code);
//     console.log(tokens);
//     oauth2Client.setCredentials(tokens);
//     console.log("Access Token:", tokens.access_token);
//     console.log("Refresh Token:", tokens.refresh_token);
//     res.send("Authentication successful! You can now upload videos.");
//   } catch (error) {
//     console.error("Error during OAuth2 callback:", error);
//     res.status(500).send("Authentication failed.");
//   }
// });

// // Endpoint to upload video
// app.post("/upload", upload.single("video"), async (req, res) => {
//   const filePath = req.file.path;
//   const { title, description, tags, privacyStatus } = req.body;

//   if (!oauth2Client.credentials) {
//     return res.status(401).send("User is not authenticated.");
//   }

//   const youtube = google.youtube({ version: "v3", auth: oauth2Client });

//   try {
//     const response = await youtube.videos.insert({
//       part: "snippet,status",
//       requestBody: {
//         snippet: {
//           title: title || "Default Title",
//           description: description || "Default Description",
//           tags: tags ? tags.split(",") : [],
//           categoryId: "22", // Category ID for 'People & Blogs'
//         },
//         status: {
//           privacyStatus: privacyStatus || "public", // public, private, or unlisted
//         },
//       },
//       media: {
//         body: fs.createReadStream(filePath),
//       },
//     });

//     // Remove the temporary uploaded file
//     fs.unlinkSync(filePath);

//     res.status(200).send({
//       message: "Video uploaded successfully",
//       videoId: response.data.id,
//     });
//   } catch (error) {
//     console.error("Error uploading video:", error);
//     res.status(500).send("Failed to upload video.");
//   }
// });

// // Start server
// app.listen(port, () => {
//   console.log(`Server is running on ${port}`);
// });

// // app.get('/generate-token', async (req, res) => {
// //     try {
// //       const { token } = await oAuth2Client.getAccessToken();
// //       res.send({ access_token: token });
// //     } catch (error) {
// //       res.status(500).send({ error: error.message });
// //     }
// //   });

// //   const oAuth2Client = new google.auth.OAuth2(
// //     CLIENT_ID, // Replace with your client ID
// //     CLIENT_SECRET, // Replace with your client secret
// //     'http://localhost:3001/oauth2callback' // Replace with your redirect URI
// //   );

// //   oAuth2Client.setCredentials({
// //     refresh_token: 'YOUR_REFRESH_TOKEN' // Replace with your refresh token
// //   });
