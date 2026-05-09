import nodemailer from "nodemailer";

export const sendEmail = async ({ to, subject, html }) => {
  const hasSmtp = process.env.SMTP_HOST && process.env.SMTP_USER && process.env.SMTP_PASS;

  if (!hasSmtp) {
    console.log("Email notification skipped in development:", { to, subject });
    return;
  }

  const transporter = nodemailer.createTransport({
    host: process.env.SMTP_HOST,
    port: Number(process.env.SMTP_PORT || 587),
    secure: false,
    auth: {
      user: process.env.SMTP_USER,
      pass: process.env.SMTP_PASS
    }
  });

  await transporter.sendMail({
    from: process.env.SMTP_FROM || "College ERP <no-reply@college-erp.local>",
    to,
    subject,
    html
  });
};
