import japa.parser.ASTHelper;
import japa.parser.JavaParser;
import japa.parser.ast.CompilationUnit;
import japa.parser.ast.PackageDeclaration;
import japa.parser.ast.body.ClassOrInterfaceDeclaration;
import japa.parser.ast.body.MethodDeclaration;
import japa.parser.ast.body.VariableDeclaratorId;
import japa.parser.ast.body.ModifierSet;
import japa.parser.ast.body.Parameter;
import japa.parser.ast.expr.FieldAccessExpr;
import japa.parser.ast.expr.MethodCallExpr;
import japa.parser.ast.expr.NameExpr;
import japa.parser.ast.expr.StringLiteralExpr;
import japa.parser.ast.stmt.BlockStmt;
import japa.parser.ast.visitor.VoidVisitorAdapter;

import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.io.ByteArrayInputStream;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.util.ArrayList;
import java.util.List;
import java.util.HashSet;
import java.nio.charset.StandardCharsets;

public class Main {

    public static void listNames(String fileName) throws Exception {
        HashSet<String> ids = new HashSet<String>();
        class IdentifierVisitor extends VoidVisitorAdapter<Void> {
            @Override
            public void visit(VariableDeclaratorId vd, Void ignore) {
                super.visit(vd, ignore);
                ids.add(vd.getName());
            }
            @Override
            public void visit(NameExpr ne, Void ignore) {
                super.visit(ne, ignore);
                ids.add(ne.getName());
            }
            @Override
            public void visit(MethodDeclaration md, Void ignore) {
                super.visit(md, ignore);
                ids.add(md.getName());
            }

            @Override
            public void visit(MethodCallExpr mc, Void ignore) {
                super.visit(mc, ignore);
                ids.add(mc.getName());
            }

            @Override
            public void visit(StringLiteralExpr sl, Void ignore) {
                super.visit(sl, ignore);
                ids.add(sl.getValue());
            }                                                
        }
        
        // mock complete class to enable parsing from method (test case)
        File temp = File.createTempFile("tempfile", ".tmp"); 
        BufferedWriter bw = new BufferedWriter(new FileWriter(temp));
        StringBuffer sb = new StringBuffer();
        sb.append("public class Main {");
        sb.append(System.lineSeparator());        
        try (BufferedReader br = new BufferedReader(new FileReader(fileName))) { //StandardCharsets.UTF_8
            String line;
            while ((line = br.readLine()) != null) {
                sb.append(line);
                sb.append(System.lineSeparator());
            }
        }
        sb.append("}");
        bw.write(sb.toString());
        bw.close();

        // reporting identifiers
        FileInputStream in = new FileInputStream(temp.getAbsolutePath());
        CompilationUnit compUnit;
        try {
            compUnit = JavaParser.parse(in);
            compUnit.accept(new IdentifierVisitor(), null);
            List<String> stopWords = java.util.Arrays.asList(new String[]{"println","java","japa","org","Override","Exception","x","i","s","hello"});
            for (String s : ids) {
                if (!stopWords.contains(s)) System.out.println(s);
            }
        } finally {
            in.close();
        }
    }

    public static void main(String[] args) throws Exception {
        String x = "hello";
        Main.listNames(args[0]);
    }
}
