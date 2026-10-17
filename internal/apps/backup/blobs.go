package backup

import (
	"crypto/sha1"
	"encoding/hex"
	"fmt"
)

// BlobSum is the name a file takes in a repository: git's own object name,
// SHA-1 over "blob <length>\0<data>", which is what GitHub's tree API
// reports. Comparing these is what lets a push tell a file that changed
// from one the repository already holds.
func BlobSum(data []byte) string {
	h := sha1.New()
	fmt.Fprintf(h, "blob %d\x00", len(data))
	h.Write(data)
	return hex.EncodeToString(h.Sum(nil))
}
