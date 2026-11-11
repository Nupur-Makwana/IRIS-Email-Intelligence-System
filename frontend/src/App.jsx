
import { useState } from "react";
import "./App.css";

const emails = [
  {
    id: 1,
    sender: "Recruitment Team",
    address: "recruitment@company.com",
    subject: "Interview Confirmation: Software Development Internship",
    preview: "Your interview is scheduled for tomorrow.",
    category: "Job/Internship",
    priority: "High",
    score: 95,
    time: "9:30 AM",
    summary:
      "Interview tomorrow, 28 Sep, at 10:00 AM. Confirm your availability and keep your resume and ID ready.",
    reason: "Urgent wording and a deadline within 24 hours.",
    body:
      "Dear Nupur,\n\nYour interview for the Software Development Internship has been scheduled for tomorrow at 10:00 AM. Please confirm your availability as soon as possible. The meeting link will be shared after confirmation.\n\nPlease keep your updated resume and identification documents ready before the interview.\n\nBest regards,\nRecruitment Team",
    replies: [
      "Thank you, I confirm my availability.",
      "Could you share the meeting link?",
      "Could we reschedule the interview?",
    ],
  },
  {
    id: 2,
    sender: "Google Security",
    address: "security@google.com",
    subject: "Account security alert",
    preview: "We noticed a sign-in to your account.",
    category: "Security",
    priority: "High",
    score: 92,
    time: "10:42 AM",
    summary:
      "A security notification reports a recent sign-in. Verify the activity through the official account security page.",
    reason: "Security-related wording requires attention.",
    body:
      "Hello,\n\nWe noticed a sign-in to your account. If this was you, no action may be needed. If you do not recognize the activity, review your account security settings through the official website.",
    replies: [
      "I recognize this activity.",
      "I will review my account security.",
    ],
  },
  {
    id: 3,
    sender: "Project Team",
    address: "project@company.com",
    subject: "Project update meeting",
    preview: "Please join the project update meeting.",
    category: "Work",
    priority: "Medium",
    score: 78,
    time: "Yesterday",
    summary:
      "The team has shared a project update meeting request. Review the details and confirm if needed.",
    reason: "Work-related information that needs attention but is not immediately urgent.",
    body:
      "Hi team,\n\nPlease join our project update meeting on Thursday at 2 PM. We will discuss the current progress, pending tasks, and next milestones.\n\nRegards,\nProject Team",
    replies: [
      "Thank you for the update. I will attend.",
      "Could you share the meeting agenda?",
    ],
  },
  {
    id: 4,
    sender: "Bank",
    address: "alerts@bank.com",
    subject: "Monthly statement",
    preview: "Your account statement is ready.",
    category: "Finance",
    priority: "Medium",
    score: 64,
    time: "Sep 26",
    summary:
      "Your monthly account statement is available. Review it through your bank's official website or app.",
    reason: "Financial information may need review but has no stated immediate deadline.",
    body:
      "Dear Customer,\n\nYour monthly account statement is ready. Please sign in through your bank's official website or application to view it.\n\nThank you.",
    replies: [
      "Thank you for the notification.",
      "I will review the statement.",
    ],
  },
  {
    id: 5,
    sender: "Weekly Digest",
    address: "digest@example.com",
    subject: "Weekly newsletter",
    preview: "Here are this week's updates.",
    category: "Other",
    priority: "Low",
    score: 18,
    time: "Sep 25",
    summary:
      "A routine weekly digest containing general updates that can be reviewed later.",
    reason: "Routine informational content without an urgent request.",
    body:
      "Hello,\n\nHere is your weekly digest with recent updates and articles. Read it whenever convenient.\n\nHave a great day!",
    replies: [
      "Thank you for sharing.",
      "I will review this later.",
    ],
  },
];

const navItems = [
  { label: "Inbox", icon: "▤" },
  { label: "Starred", icon: "☆" },
  { label: "Sent", icon: "➤" },
  { label: "Drafts", icon: "▧" },
  { label: "Archive", icon: "▣" },
  { label: "Trash", icon: "♲" },
];

function App() {
  const [selectedId, setSelectedId] = useState(1);
  const [activeNav, setActiveNav] = useState("Inbox");
  const [filter, setFilter] = useState("All");
  const [search, setSearch] = useState("");
  const [compact, setCompact] = useState(true);
  const [showSummary, setShowSummary] = useState(true);
  const [showReplies, setShowReplies] = useState(true);
  const [notice, setNotice] = useState("");
  const [selectedIds, setSelectedIds] = useState([]);
  const [starredIds, setStarredIds] = useState([]);
  const [archivedIds, setArchivedIds] = useState([]);
  const [readIds, setReadIds] = useState([]);
  const [deletedIds, setDeletedIds] = useState([]);
  const [snoozedIds, setSnoozedIds] = useState([]);
  const [sentReplies, setSentReplies] = useState([]);
  const [draft, setDraft] = useState("");
  const [composing, setComposing] = useState(false);
  const [replying, setReplying] = useState(false);
  const [replyText, setReplyText] = useState("");
  const [customPriorities, setCustomPriorities] = useState({});
  const [reminders, setReminders] = useState([]);
  const [reminderIds, setReminderIds] = useState([]);
  const [showReminder, setShowReminder] = useState(false);
  const [reminderDate, setReminderDate] = useState("2026-10-26T10:00");
  const [reminderEmailId, setReminderEmailId] = useState(1);
  const [reminderLabel, setReminderLabel] = useState("");
  const [showClean, setShowClean] = useState(false);
  const [cleanIds, setCleanIds] = useState([]);
  const [recoveryIds, setRecoveryIds] = useState([]);
  const [dashboardRange, setDashboardRange] = useState("7 days");
  const [settings, setSettings] = useState({
    privacy: true,
    reminders: true,
    explain: true,
    categories: true,
    autoClean: false,
    learning: true,
  });
  const [aiEnabled, setAiEnabled] = useState(true);
  const [showDetails, setShowDetails] = useState(false);
  const [showUndo, setShowUndo] = useState(false);
  const [lastAction, setLastAction] = useState(null);

  const selected = emails.find((email) => email.id === selectedId) || emails[0];
  const getPriority = (email) =>
    customPriorities[email.id] || email.priority;

  const activeEmails = emails.filter(
    (email) =>
      !archivedIds.includes(email.id) &&
      !deletedIds.includes(email.id) &&
      !snoozedIds.includes(email.id) &&
      !cleanIds.includes(email.id) &&
      !recoveryIds.includes(email.id)
  );

  const visibleEmails = emails.filter((email) => {
    const priority = getPriority(email);
    const matchesSearch =
      `${email.sender} ${email.subject} ${email.preview} ${email.category}`
        .toLowerCase()
        .includes(search.toLowerCase());
    const matchesFilter =
      filter === "All" || priority === filter;
    const matchesNav =
      activeNav === "Inbox"
        ? !archivedIds.includes(email.id) &&
          !deletedIds.includes(email.id) &&
          !snoozedIds.includes(email.id) &&
          !cleanIds.includes(email.id) &&
          !recoveryIds.includes(email.id)
        : activeNav === "Starred"
          ? starredIds.includes(email.id)
          : activeNav === "Sent"
            ? sentReplies.includes(email.id)
            : activeNav === "Drafts"
              ? Boolean(draft)
              : activeNav === "Archive"
                ? archivedIds.includes(email.id)
                : activeNav === "Trash"
                  ? deletedIds.includes(email.id)
                  : activeNav === "Recovery"
                    ? recoveryIds.includes(email.id)
                    : activeNav === "Reminders"
                      ? reminderIds.includes(email.id)
                      : true;
    return matchesSearch && matchesFilter && matchesNav;
  });

  const counts = {
    High: activeEmails.filter((email) => getPriority(email) === "High").length,
    Medium: activeEmails.filter((email) => getPriority(email) === "Medium").length,
    Low: activeEmails.filter((email) => getPriority(email) === "Low").length,
  };

  function toggleSelected(id) {
    setSelectedIds((current) =>
      current.includes(id)
        ? current.filter((item) => item !== id)
        : [...current, id]
    );
  }

  function selectNav(label) {
    setActiveNav(label);
    setNotice("");
    setFilter("All");
    if (label === "Compose") {
      setComposing(true);
      setDraft("");
      return;
    }
    setComposing(false);
  }

  function applyAction(action, ids = [selectedId]) {
    const validIds = ids.filter((id) => emails.some((email) => email.id === id));
    setLastAction({ action, ids: validIds });
    if (action === "Archive") {
      setArchivedIds((current) => [...new Set([...current, ...validIds])]);
    } else if (action === "Delete") {
      setDeletedIds((current) => [...new Set([...current, ...validIds])]);
    } else if (action === "Snooze") {
      setSnoozedIds((current) => [...new Set([...current, ...validIds])]);
    } else if (action === "Mark read") {
      setReadIds((current) => [...new Set([...current, ...validIds])]);
    } else if (action === "Star") {
      setStarredIds((current) => [...new Set([...current, ...validIds])]);
    } else if (action === "Clean") {
      setCleanIds((current) => [...new Set([...current, ...validIds])]);
    }
    setSelectedIds([]);
    setNotice(`${validIds.length} email${validIds.length === 1 ? "" : "s"} ${action.toLowerCase()}ed.`);
    setShowUndo(true);
  }

  function undoAction() {
    if (!lastAction) return;
    const { action, ids } = lastAction;
    if (action === "Archive") setArchivedIds((current) => current.filter((id) => !ids.includes(id)));
    if (action === "Delete") setDeletedIds((current) => current.filter((id) => !ids.includes(id)));
    if (action === "Snooze") setSnoozedIds((current) => current.filter((id) => !ids.includes(id)));
    if (action === "Mark read") setReadIds((current) => current.filter((id) => !ids.includes(id)));
    if (action === "Star") setStarredIds((current) => current.filter((id) => !ids.includes(id)));
    if (action === "Clean") setCleanIds((current) => current.filter((id) => !ids.includes(id)));
    setNotice("Last action undone.");
    setShowUndo(false);
    setLastAction(null);
  }

  function sendReply(text) {
    if (!text.trim()) return;
    setNotice("Demo only: connect the backend to send this reply.");
    setReplyText(text);
    setReplying(false);
  }

  function scheduleReminder() {
    const label = reminderLabel.trim() || selected.subject;
    setReminders((current) => [
      ...current,
      { id: Date.now(), emailId: reminderEmailId, label, date: reminderDate },
    ]);
    setReminderIds((current) => [...new Set([...current, reminderEmailId])]);
    setShowReminder(false);
    setNotice("Reminder saved in this demo session.");
  }

  const topNav = ["Inbox", "Starred", "Sent", "Drafts", "Archive", "Trash"];

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <button className="brand" onClick={() => selectNav("Inbox")}>
          <span className="brand-mark" />
          <span>IRIS<small>AI Email Workspace</small></span>
        </button>

        <button className="compose-btn" onClick={() => selectNav("Compose")}>
          <span>＋</span> Compose
        </button>

        <nav className="main-nav">
          {topNav.map((item) => (
            <button
              key={item}
              className={`nav-item ${activeNav === item ? "active" : ""}`}
              onClick={() => selectNav(item)}
            >
              <span className="nav-icon">
                {{
                  Inbox: "▤",
                  Starred: "☆",
                  Sent: "➤",
                  Drafts: "▧",
                  Archive: "▣",
                  Trash: "♲",
                }[item]}
              </span>
              <span>{item}</span>
              {item === "Inbox" && <span className="nav-count">{activeEmails.length}</span>}
            </button>
          ))}
        </nav>

        <div className="nav-section-label">AI TOOLS</div>
        <nav className="main-nav">
          {[
            ["Dashboard", "▦"],
            ["Opportunities", "✧"],
            ["Smart Clean", "⌁"],
            ["Recovery", "↶"],
            ["Reminders", "♧"],
            ["Settings", "⚙"],
          ].map(([item, icon]) => (
            <button
              key={item}
              className={`nav-item ${activeNav === item ? "active" : ""}`}
              onClick={() => selectNav(item)}
            >
              <span className="nav-icon">{icon}</span>
              <span>{item}</span>
              {item === "Reminders" && reminders.length > 0 && (
                <span className="nav-count">{reminders.length}</span>
              )}
            </button>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="engine-row">
            <span>AI engine</span>
            <button
              className={`switch ${aiEnabled ? "on" : ""}`}
              aria-label="Toggle AI engine"
              onClick={() => setAiEnabled((value) => !value)}
            >
              <span />
            </button>
          </div>
          <div className="sidebar-caption">Smarter emails. Better productivity.</div>
        </div>
      </aside>

      <main className="main-area">
        <header className="topbar">
          <label className="search-box">
            <span>⌕</span>
            <input
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Search emails..."
            />
            {search && (
              <button className="clear-search" onClick={() => setSearch("")}>×</button>
            )}
          </label>
          <div className="topbar-user">
            <span className="online-dot" />
            <span className="avatar small-avatar">N</span>
            <span>Nupur</span>
          </div>
        </header>

        {notice && (
          <div className="notice">
            <span>{notice}</span>
            {showUndo && <button onClick={undoAction}>Undo</button>}
            <button onClick={() => setNotice("")}>×</button>
          </div>
        )}

        {activeNav === "Dashboard" ? (
          <section className="content-page">
            <div className="page-heading">
              <div><span className="eyebrow">YOUR EMAIL OVERVIEW</span><h1>Dashboard</h1></div>
              <select value={dashboardRange} onChange={(event) => setDashboardRange(event.target.value)}>
                <option>Today</option><option>7 days</option><option>30 days</option>
              </select>
            </div>
            <div className="metric-grid">
              <Metric label="Emails in demo" value={emails.length} note="Sample inbox" />
              <Metric label="High priority" value={counts.High} note="Needs attention" />
              <Metric label="Medium priority" value={counts.Medium} note="Review soon" />
              <Metric label="Low priority" value={counts.Low} note="Can wait" />
            </div>
            <div className="dashboard-grid">
              <section className="panel">
                <h3>Priority distribution</h3>
                {["High", "Medium", "Low"].map((priority) => (
                  <div className="bar-row" key={priority}>
                    <span>{priority}</span><div className="bar-track"><div className={`bar-fill ${priority.toLowerCase()}`} style={{ width: `${(counts[priority] / Math.max(activeEmails.length, 1)) * 100}%` }} /></div><b>{counts[priority]}</b>
                  </div>
                ))}
              </section>
              <section className="panel">
                <h3>Category overview</h3>
                {[...new Set(emails.map((email) => email.category))].map((category) => (
                  <div className="category-row" key={category}><span>{category}</span><b>{emails.filter((email) => email.category === category).length}</b></div>
                ))}
              </section>
            </div>
          </section>
        ) : activeNav === "Settings" ? (
          <section className="content-page">
            <div className="page-heading"><div><span className="eyebrow">PERSONALIZE YOUR WORKSPACE</span><h1>Settings</h1></div></div>
            <section className="panel settings-panel">
              {[
                ["privacy", "Privacy Guardian", "Future setting: detect suspicious links and phishing attempts."],
                ["reminders", "Smart Reminders", "Allow reminder controls in the interface."],
                ["explain", "Explainable AI", "Show why each email received its priority."],
                ["categories", "Category tags", "Show email category labels."],
                ["autoClean", "Auto clean", "Demo preference only; no emails are automatically removed."],
                ["learning", "Learn from my corrections", "Future setting: use corrections to improve predictions."],
              ].map(([key, title, description]) => (
                <div className="setting-row" key={key}>
                  <div><strong>{title}</strong><p>{description}</p></div>
                  <button className={`switch ${settings[key] ? "on" : ""}`} onClick={() => setSettings((current) => ({ ...current, [key]: !current[key] }))} aria-label={`Toggle ${title}`}><span /></button>
                </div>
              ))}
            </section>
            <p className="muted-note">These preferences currently affect the prototype only.</p>
          </section>
        ) : activeNav === "Smart Clean" ? (
          <section className="content-page">
            <div className="page-heading"><div><span className="eyebrow">DECLUTTER YOUR INBOX</span><h1>Smart Clean</h1><p>Review low-priority messages before moving them.</p></div></div>
            <div className="panel">
              {emails.filter((email) => getPriority(email) === "Low" && !cleanIds.includes(email.id) && !archivedIds.includes(email.id) && !deletedIds.includes(email.id)).map((email) => (
                <div className="clean-row" key={email.id}><div><strong>{email.sender}</strong><p>{email.subject}</p></div><PriorityBadge priority="Low" score={email.score} /><button className="button-secondary" onClick={() => applyAction("Archive", [email.id])}>Archive</button><button className="button-primary small-button" onClick={() => { setCleanIds((current) => [...new Set([...current, email.id])]); setNotice("Email moved to Recovery in this demo."); }}>Move to Recovery</button></div>
              ))}
              <p className="muted-note">No email is permanently deleted by Smart Clean.</p>
            </div>
          </section>
        ) : activeNav === "Opportunities" ? (
          <section className="content-page">
            <div className="page-heading"><div><span className="eyebrow">CAREER & GROWTH</span><h1>Opportunities</h1><p>Emails that may contain jobs, internships, events, or learning opportunities.</p></div></div>
            <div className="panel">
              {emails.filter((email) => /job|internship|event/i.test(email.category + " " + email.subject)).map((email) => (
                <button className="opportunity-row" key={email.id} onClick={() => { setSelectedId(email.id); setActiveNav("Inbox"); }}>
                  <span className="opportunity-icon">✧</span><span><strong>{email.subject}</strong><small>{email.sender} · {email.category}</small></span><PriorityBadge priority={getPriority(email)} score={email.score} />
                </button>
              ))}
            </div>
          </section>
        ) : activeNav === "Recovery" ? (
          <section className="content-page">
            <div className="page-heading"><div><span className="eyebrow">YOUR SAFETY NET</span><h1>Recovery</h1><p>Restore emails moved to Recovery in this demo.</p></div></div>
            <div className="panel">
              {emails.filter((email) => cleanIds.includes(email.id) || recoveryIds.includes(email.id)).map((email) => (
                <div className="clean-row" key={email.id}><div><strong>{email.sender}</strong><p>{email.subject}</p></div><button className="button-primary small-button" onClick={() => { setCleanIds((current) => current.filter((id) => id !== email.id)); setRecoveryIds((current) => current.filter((id) => id !== email.id)); setNotice("Email restored to inbox."); }}>Restore</button></div>
              ))}
              {!emails.some((email) => cleanIds.includes(email.id) || recoveryIds.includes(email.id)) && <p className="empty-state">Nothing to recover yet.</p>}
            </div>
          </section>
        ) : activeNav === "Reminders" ? (
          <section className="content-page">
            <div className="page-heading"><div><span className="eyebrow">DON'T MISS WHAT MATTERS</span><h1>Reminders</h1><p>Reminders saved in this browser session.</p></div><button className="button-primary" onClick={() => { setReminderEmailId(selectedId); setShowReminder(true); }}>＋ Add reminder</button></div>
            <div className="panel">
              {reminders.map((reminder) => <div className="clean-row" key={reminder.id}><div><strong>{reminder.label}</strong><p>{new Date(reminder.date).toLocaleString()}</p></div><button className="button-secondary" onClick={() => setReminders((current) => current.filter((item) => item.id !== reminder.id))}>Remove</button></div>)}
              {reminders.length === 0 && <p className="empty-state">No reminders yet. Select an email and add a reminder.</p>}
            </div>
          </section>
        ) : (
          <section className="inbox-layout">
            <div className="mail-list-pane">
              <div className="inbox-heading">
                <div><span className="eyebrow">YOUR WORKSPACE</span><h1>{activeNav}</h1><p>{visibleEmails.length} messages in this view</p></div>
                <button className="icon-button" title="Refresh demo list" onClick={() => setNotice("Demo inbox refreshed.")}>↻</button>
              </div>

              <div className="welcome-card">
                <div className="welcome-top"><span className="sparkle">✦</span><span>IRIS INTELLIGENCE</span><span className="live-pill"><i /> Demo mode</span></div>
                <h2>Good morning, Nupur.</h2>
                <p>Here’s what needs your attention.</p>
                <div className="welcome-metrics">
                  <div><strong>{counts.High}</strong><span>High priority</span></div>
                  <div><strong>{counts.Medium}</strong><span>Medium</span></div>
                  <div><strong>{counts.Low}</strong><span>Low priority</span></div>
                </div>
              </div>

              <div className="filter-row">
                {["All", "High", "Medium", "Low"].map((item) => (
                  <button key={item} className={`filter-chip ${filter === item ? "selected" : ""}`} onClick={() => setFilter(item)}>{item}</button>
                ))}
                <button className="density-toggle" onClick={() => setCompact((value) => !value)}>{compact ? "Comfortable view" : "Compact view"}</button>
              </div>

              {selectedIds.length > 0 && (
                <div className="bulk-toolbar">
                  <strong>{selectedIds.length} selected</strong>
                  {["Archive", "Mark read", "Snooze", "Delete"].map((action) => (
                    <button key={action} onClick={() => applyAction(action, selectedIds)}>{action}</button>
                  ))}
                </div>
              )}

              <div className="email-table">
                <div className="list-label">YOUR MESSAGES</div>
                {visibleEmails.map((email) => (
                  <div key={email.id} className={`email-row ${selectedId === email.id ? "selected" : ""} ${compact ? "compact" : ""} ${readIds.includes(email.id) ? "read" : ""}`}>
                    <input type="checkbox" checked={selectedIds.includes(email.id)} onChange={() => toggleSelected(email.id)} aria-label={`Select ${email.subject}`} />
                    <button className="email-select" onClick={() => { setSelectedId(email.id); setComposing(false); setShowDetails(false); setReadIds((current) => [...new Set([...current, email.id])]); }}>
                      <span className={`sender-avatar avatar-${email.id}`}>{email.sender.charAt(0)}</span>
                      <span className="email-copy">
                        <strong>{email.sender}</strong>
                        <span className="email-subject">{email.subject}</span>
                        {!compact && <span className="email-preview">{email.preview}</span>}
                      </span>
                      <span className="email-tags">
                        {settings.categories && <span className="category-pill">{email.category}</span>}
                        <PriorityBadge priority={getPriority(email)} score={email.score} />
                      </span>
                      <span className="email-time">{email.time}</span>
                    </button>
                    <button className={`star-button ${starredIds.includes(email.id) ? "starred" : ""}`} title="Star email" onClick={() => setStarredIds((current) => current.includes(email.id) ? current.filter((id) => id !== email.id) : [...current, email.id])}>★</button>
                  </div>
                ))}
                {visibleEmails.length === 0 && <p className="empty-state">No emails found. Try another search or filter.</p>}
              </div>
              <div className="keyboard-hints"><span>Tip: select messages for bulk actions.</span><span>{visibleEmails.length} shown</span></div>
            </div>

            <div className="message-pane">
              {composing ? (
                <div className="compose-view">
                  <div className="message-header"><span className="eyebrow">NEW MESSAGE</span><button className="icon-button" onClick={() => setComposing(false)}>×</button></div>
                  <h2>Compose email</h2>
                  <form onSubmit={(event) => { event.preventDefault(); setNotice("Demo only: connect the backend to send emails."); setComposing(false); setDraft(""); }}>
                    <label>To<input required placeholder="recipient@example.com" /></label>
                    <label>Subject<input required placeholder="Email subject" /></label>
                    <label>Message<textarea required rows="8" value={draft} onChange={(event) => setDraft(event.target.value)} placeholder="Write your message..." /></label>
                    <button className="button-primary" type="submit">Send email</button>
                    <p className="muted-note">Demo only. This form does not send email yet.</p>
                  </form>
                </div>
              ) : (
                <>
                  <div className="message-header">
                    <div><span className="eyebrow">EMAIL DETAILS</span><span className="message-number">Message #{selected.id}</span></div>
                    <div className="message-header-actions">
                      <button className={`icon-button ${starredIds.includes(selected.id) ? "starred" : ""}`} title="Star" onClick={() => setStarredIds((current) => current.includes(selected.id) ? current.filter((id) => id !== selected.id) : [...current, selected.id])}>★</button>
                      <button className="icon-button" title="Archive" onClick={() => applyAction("Archive")}>▣</button>
                      <button className="icon-button" title="More details" onClick={() => setShowDetails((value) => !value)}>•••</button>
                    </div>
                  </div>

                  <h2 className="message-subject">{selected.subject}</h2>
                  <div className="sender-line">
                    <span className={`sender-avatar avatar-${selected.id}`}>{selected.sender.charAt(0)}</span>
                    <div><strong>{selected.sender}</strong><span>{selected.address}</span></div>
                    <span className="message-time">{selected.time}</span>
                  </div>

                  {showDetails && <div className="detail-strip"><span>From: {selected.address}</span><span>Category: {selected.category}</span><span>Priority score: {selected.score}</span></div>}

                  {settings.reminders && (
                    <div className="reminder-banner">
                      <div><span className="reminder-icon">◷</span><span><strong>Remember this email?</strong><small>Create a reminder for a deadline or follow-up.</small></span></div>
                      <button className="button-secondary" onClick={() => { setReminderEmailId(selected.id); setReminderLabel(selected.subject); setShowReminder(true); }}>＋ Reminder</button>
                    </div>
                  )}

                  {aiEnabled && (
                    <section className="ai-card">
                      <div className="ai-card-heading"><div><span className="ai-icon">✦</span><div><strong>AI Insights</strong><small>Generated for this email</small></div></div><span className="ai-status"><i /> AI on</span></div>
                      <div className="ai-meta">
                        {settings.categories && <span className="category-pill">{selected.category}</span>}
                        <PriorityBadge priority={getPriority(selected)} score={selected.score} />
                      </div>
                      {showSummary && <div className="ai-summary"><h3>AI SUMMARY</h3><p>{selected.summary}</p></div>}
                      {settings.explain && <div className="ai-explanation"><span className="explain-icon">ⓘ</span><p><strong>Why {getPriority(selected)}?</strong> {selected.reason}</p></div>}
                      <div className="ai-card-footer">
                        <button onClick={() => setShowSummary((value) => !value)}>{showSummary ? "Hide summary" : "Show summary"}</button>
                        <button onClick={() => setShowReplies((value) => !value)}>{showReplies ? "Hide replies" : "Show replies"}</button>
                      </div>
                    </section>
                  )}

                  {showReplies && aiEnabled && (
                    <section className="smart-replies">
                      <div className="section-heading"><h3>Smart Replies</h3><span>AI SUGGESTIONS</span></div>
                      <div className="reply-options">
                        {selected.replies.map((reply) => <button key={reply} className="reply-chip" onClick={() => { setReplyText(reply); setReplying(true); }}>{reply}<span>↗</span></button>)}
                      </div>
                    </section>
                  )}

                  {replying && (
                    <form className="reply-composer" onSubmit={(event) => { event.preventDefault(); sendReply(replyText); }}>
                      <div className="reply-composer-heading"><strong>Reply to {selected.sender}</strong><button type="button" className="icon-button" onClick={() => setReplying(false)}>×</button></div>
                      <textarea value={replyText} onChange={(event) => setReplyText(event.target.value)} rows="4" />
                      <div className="reply-composer-actions"><button type="button" className="button-secondary" onClick={() => setReplying(false)}>Cancel</button><button type="submit" className="button-primary">Send reply</button></div>
                    </form>
                  )}

                  <div className="message-body">
                    {selected.body.split("\n").map((line, index) => line ? <p key={index}>{line}</p> : <div className="body-space" key={index} />)}
                  </div>

                  <div className="message-actions">
                    <button className="button-primary" onClick={() => { setReplyText(""); setReplying(true); }}>↶ Reply</button>
                    <button className="button-secondary" onClick={() => applyAction("Archive")}>▣ Archive</button>
                    <button className="button-secondary" onClick={() => applyAction("Snooze")}>◷ Snooze</button>
                    <button className="button-secondary" onClick={() => applyAction("Delete")}>♲ Delete</button>
                  </div>

                  <div className="priority-teaching">
                    <span className="eyebrow">WRONG PRIORITY? TEACH IRIS</span>
                    <p>Correct this email's label for the current demo session.</p>
                    <div>{["High", "Medium", "Low"].map((priority) => <button key={priority} className={`priority-choice ${getPriority(selected) === priority ? "chosen" : ""}`} onClick={() => { setCustomPriorities((current) => ({ ...current, [selected.id]: priority })); setNotice(`Priority changed to ${priority} for this demo.`); }}>{priority}</button>)}</div>
                  </div>

                  <p className="privacy-note">IRIS suggests. You decide. Nothing is sent or permanently deleted by this prototype.</p>
                </>
              )}
            </div>
          </section>
        )}
      </main>
      
      {showReminder && (
        <div className="modal-backdrop" onMouseDown={(event) => { if (event.target === event.currentTarget) setShowReminder(false); }}>
          <form className="modal-card" onSubmit={(event) => { event.preventDefault(); scheduleReminder(); }}>
            <div className="modal-heading"><div><span className="eyebrow">STAY ON TRACK</span><h2>Set a reminder</h2></div><button type="button" className="icon-button" onClick={() => setShowReminder(false)}>×</button></div>
            <label>Reminder title<input value={reminderLabel} onChange={(event) => setReminderLabel(event.target.value)} placeholder={selected.subject} /></label>
            <label>Date and time<input type="datetime-local" value={reminderDate} onChange={(event) => setReminderDate(event.target.value)} required /></label>
            <p className="muted-note">This reminder stays in the current demo session. Notifications and calendar sync are not connected.</p>
            <div className="modal-actions"><button type="button" className="button-secondary" onClick={() => setShowReminder(false)}>Cancel</button><button className="button-primary" type="submit">Save reminder</button></div>
          </form>
        </div>
      )}
    </div>
  );
}
function ReminderToast({ title, time, place, onClose }) {
  return (
    <div className="reminder-toast" role="alert">
      <div className="reminder-toast-content">
        <strong>{title}</strong>
        <span>
          {time}
          {place && ` · ${place}`}
        </span>
      </div>

      <button
        className="reminder-toast-close"
        onClick={onClose}
        aria-label="Dismiss reminder"
      >
        ×
      </button>
    </div>
  );
}
function PriorityBadge({ priority, score }) {
  return <span className={`priority-badge ${priority.toLowerCase()}`}><i />{priority}{score !== undefined && <span className="priority-score"> {score}</span>}</span>;
}

function Metric({ label, value, note }) {
  return <div className="metric-card"><span>{label}</span><strong>{value}</strong><small>{note}</small></div>;
}

export default App;
