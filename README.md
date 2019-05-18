# Drop Docs

Drop Docs uses(abuses) the lack of storage limitation of google docs to its advantage.
The uploading file is split into chunks and the binary data gets converted to hex format and uploaded into several google docs.

[Here](https://support.google.com/drive/answer/37603?hl=en "Here") and [here](https://computer.howstuffworks.com/internet/basics/google-docs2.htm) you can find the official limitations given by google.

So accordiung to Google you can save up to **500kb** in one Google Document, with a document limit of **5000**.

## Setup

To get started follow the [Google Docs API instructions])(https://developers.google.com/docs/api/quickstart/python) and [Google Drive API instructions](https://developers.google.com/drive/api/v3/quickstart/python),then download the credentials.json(same for google docs and drive) file and move it in the project folder.
