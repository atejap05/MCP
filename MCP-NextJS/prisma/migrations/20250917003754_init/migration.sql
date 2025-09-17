-- CreateTable
CREATE TABLE "Bookmark" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "url" TEXT NOT NULL,
    "title" TEXT NOT NULL,
    "userId" TEXT NOT NULL,
    "notes" TEXT,
    "tags" TEXT,
    "favicon" TEXT,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL
);

-- CreateTable
CREATE TABLE "Category" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "name" TEXT NOT NULL,
    "color" TEXT NOT NULL DEFAULT '#0070f3',
    "userId" TEXT NOT NULL,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL
);

-- CreateTable
CREATE TABLE "BookmarkCategory" (
    "bookmarkId" TEXT NOT NULL,
    "categoryId" TEXT NOT NULL,
    "assignedAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY ("bookmarkId", "categoryId"),
    CONSTRAINT "BookmarkCategory_bookmarkId_fkey" FOREIGN KEY ("bookmarkId") REFERENCES "Bookmark" ("id") ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT "BookmarkCategory_categoryId_fkey" FOREIGN KEY ("categoryId") REFERENCES "Category" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- CreateIndex
CREATE INDEX "Bookmark_userId_idx" ON "Bookmark"("userId");

-- CreateIndex
CREATE INDEX "Bookmark_createdAt_idx" ON "Bookmark"("createdAt");

-- CreateIndex
CREATE INDEX "Bookmark_userId_createdAt_idx" ON "Bookmark"("userId", "createdAt");

-- CreateIndex
CREATE INDEX "Category_userId_idx" ON "Category"("userId");

-- CreateIndex
CREATE UNIQUE INDEX "Category_userId_name_key" ON "Category"("userId", "name");

-- CreateIndex
CREATE INDEX "BookmarkCategory_bookmarkId_idx" ON "BookmarkCategory"("bookmarkId");

-- CreateIndex
CREATE INDEX "BookmarkCategory_categoryId_idx" ON "BookmarkCategory"("categoryId");
