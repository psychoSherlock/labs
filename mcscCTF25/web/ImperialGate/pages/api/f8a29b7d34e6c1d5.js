export default function handler(req, res) {
  // 1. Validate request method
  if (req.method !== "GET") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  // 2. Check origin header - must match the server host
  const origin = req.headers.origin || "";
  const host = req.headers.host || "";

  // 3. Check referer - must come from the will page specifically
  const referer = req.headers.referer || "";
  const refererURL = referer ? new URL(referer) : null;
  const refererPath = refererURL ? refererURL.pathname : "";
  const isFromWillPage = refererPath.includes("/will");

  // 4. Custom secret header that the client code will send
  const secretHeader = req.headers["x-f8a29b7d"] || "";
  const validSecret = "f8a29b7d34e6c1d5";

  // 5. Comprehensive validation - all conditions must be true
  const isValidOrigin = origin.includes(host) || origin === ""; // empty is likely server-side/same-origin
  const isValidRequest =
    isValidOrigin && isFromWillPage && secretHeader === validSecret;

  // 6. If any validation fails, return a 403 error
  if (!isValidRequest) {
    // Get the client IP address - properly handle Nginx proxy headers
    // Nginx typically sets X-Real-IP or includes the real IP in X-Forwarded-For
    const realIp = req.headers["x-real-ip"]; // Nginx specific header
    const forwardedFor = req.headers["x-forwarded-for"] || "";

    // Prioritize headers in this order: X-Real-IP, X-Forwarded-For, socket.remoteAddress
    let clientIp = "Unknown";
    if (realIp) {
      clientIp = realIp; // Use X-Real-IP if available (most reliable with Nginx)
    } else if (forwardedFor) {
      // X-Forwarded-For may contain multiple IPs (client, proxy1, proxy2, ...)
      // The leftmost is typically the client's real IP
      clientIp = forwardedFor.split(",")[0].trim();
    } else if (req.socket && req.socket.remoteAddress) {
      clientIp = req.socket.remoteAddress;
    }

    const timestamp = new Date().toISOString();
    const logEntry = `[${timestamp}] Unauthorized access attempt from IP: ${clientIp} | Origin: ${
      origin || "None"
    } | Referer: ${refererPath || "None"} | Headers: ${JSON.stringify(
      req.headers
    )}\n`;

    // Log to console
    console.log("Unauthorized flag access attempt", {
      ip: clientIp,
      origin,
      host,
      refererPath,
      hasValidSecret: secretHeader === validSecret,
      headers: req.headers, // Log all headers for debugging
    });

    // Log to file system with error handling
    const fs = require("fs");
    const path = require("path");
    const logFilePath = path.join(process.cwd(), "access_logs.txt");

    try {
      fs.appendFileSync(logFilePath, logEntry);
    } catch (error) {
      console.error("Error writing to access log:", error);

      // Try to create log directory if it doesn't exist
      try {
        const dir = path.dirname(logFilePath);
        if (!fs.existsSync(dir)) {
          fs.mkdirSync(dir, { recursive: true });
          fs.appendFileSync(logFilePath, logEntry);
        }
      } catch (mkdirError) {
        console.error("Failed to create log directory:", mkdirError);
      }
    }

    return res.status(403).json({
      error: "Access denied - The Emperor protects his sacred knowledge.",
    });
  }

  // 7. All validations passed - return the flag
  return res.status(200).json({
    flag: "mcsc{thr0ugh_th3_sacr3d_m1ddl3war3}",
  });
}
