package gamesui

import (
	"image/color"

	"github.com/makiuchi-d/gozxing"
	"github.com/makiuchi-d/gozxing/qrcode"
)

// qrOf is a link's QR code; nil when it cannot be made.
func qrOf(text string) *gozxing.BitMatrix {
	if text == "" {
		return nil
	}
	m, err := qrcode.NewQRCodeWriter().EncodeWithoutHint(text, gozxing.BarcodeFormat_QR_CODE, 0, 0)
	if err != nil {
		return nil
	}
	return m
}

// drawQR draws a QR code side units wide, dark modules on white with its
// quiet zone; only the white while there is none.
func drawQR(pn pen, m *gozxing.BitMatrix, side float64) {
	pn.Color(white)
	pn.Rect(0, 0, side, side)
	pn.Fill()
	if m == nil {
		return
	}
	k := side / float64(m.GetWidth())
	pn.Color(color.NRGBA{0x1F, 0x1B, 0x17, 255})
	for y := range m.GetHeight() {
		for x := range m.GetWidth() {
			if m.Get(x, y) {
				pn.Rect(float64(x)*k, float64(y)*k, k+0.3, k+0.3) // a little over, no seams
			}
		}
	}
	pn.Fill()
}
