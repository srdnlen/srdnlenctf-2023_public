using System.Text;
using System;
namespace Core
{
    public static class FlagChecker
    {
        public static string Check(string flag)
        {
            byte[] flag_encrypted = new byte[] { 0x44, 0x55, 0x33, 0x0A, 0x2A, 0x13, 0x47, 0x3B, 0x58, 0x60, 0x2F, 0x1B, 0x49, 0x59, 0x09, 0x1F, 0x42, 0x1E, 0x51,
                0x20, 0x52, 0x61, 0x0F, 0x33, 0x07, 0x54, 0x4A, 0x06, 0x62, 0x59, 0x78, 0x33, 0x54, 0x32, 0x29, 0x47, 0x73, 0x5B, 0x2E };
            string key = "7'WdFv)@/Spwy/:@vp5RbPkl3$:YS";
            string flag_enc_str = Encoding.ASCII.GetString(flag_encrypted);
            string flag_dc = EncryptOrDecrypt(flag_enc_str, key);
            if (flag_dc.Equals(flag))
            {
                return "Output:    Correct flag!!";
            }
            else
            {
                return "Output:    Wrong Flag!!!";
            }

        }
        static string EncryptOrDecrypt(string text, string key)
        {
            var result = new StringBuilder();

            for (int c = 0; c < text.Length; c++)
                result.Append((char)((uint)text[c] ^ (uint)key[c % key.Length]));

            return result.ToString();
        }
    }
}