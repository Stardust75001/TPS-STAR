import axios from "axios";
import fs from "fs";

const API = "https://apiv2.ahrefs.com";
const TOKEN = process.env.AHREFS_API_KEY;
const SITE = process.env.STORE_URL;

(async () => {
  if (!TOKEN || !SITE) {
    console.error("❌ Missing AHREFS_API_KEY or STORE_URL in environment variables.");
    process.exit(1);
  }
  try {
    const res = await axios.get(API, {
      params: {
        token: TOKEN,
        from: "domain_rating",
        target: SITE,
        mode: "domain",
        output: "json"
      }
    });
    fs.writeFileSync("ahrefs-report.json", JSON.stringify(res.data, null, 2));
    console.log("✅ Ahrefs report saved");
  } catch (err) {
    console.error("❌ Error fetching Ahrefs report:", err.message);
    process.exit(2);
  }
})();
