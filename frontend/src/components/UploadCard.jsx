function UploadCard() {
  return (
    <div className="upload-card">

      <h2>Upload Log File</h2>

      <p>
        Supported formats:
        <br />
        .log &nbsp; .csv &nbsp; .txt
      </p>

      <input type="file" />

      <br />
      <br />

      <button>Analyze</button>

    </div>
  );
}

export default UploadCard;